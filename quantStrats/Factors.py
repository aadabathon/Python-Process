import argparse
import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import pandas_datareader.data as web; web.DataReader("F-F_Research_Data_Factors_daily","famafrench")[0].to_csv("C:\Users\adams\Python-Projects\quantStrats\DATAsets\factors.csv.xlsx") 
import yfinance

@dataclass
class FactorResult:
    alpha_daily: float
    betas: pd.Series
    r2: float
    nobs: int

def _to_datetime_index(df: pd.DataFrame, date_col: str = None) -> pd.DataFrame:
    if date_col and date_col in df.columns:
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.copy()
        df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def load_stock_returns_from_csv(path: str, date_col: str = None, price_col: str = None, ret_col: str = None) -> pd.Series:
    df = pd.read_csv(path)
    df = _to_datetime_index(df, date_col=date_col)
    cols = df.columns.tolist()

    if ret_col and ret_col in cols:
        r = df[ret_col].astype(float)
        return r.rename("stock_ret")

    if price_col and price_col in cols:
        px = df[price_col].astype(float)
    else:
        price_like = [c for c in cols if c.lower() in ("adj close", "adjclose", "close", "price", "px", "adj_close")]
        if not price_like:
            raise ValueError("Could not infer price column. Pass --stock-price-col or --stock-ret-col.")
        px = df[price_like[0]].astype(float)

    r = px.pct_change().dropna()
    return r.rename("stock_ret")

def try_load_stock_returns_yfinance(ticker: str, start: str, end: str) -> pd.Series:
    try:
        import yfinance as yf
    except Exception as e:
        raise RuntimeError("yfinance not installed. Install with: pip install yfinance") from e

    data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if data is None or data.empty:
        raise RuntimeError("No data returned from yfinance.")
    if "Close" not in data.columns:
        raise RuntimeError("Expected Close column from yfinance.")
    r = data["Close"].pct_change().dropna()
    r.name = "stock_ret"
    r.index = pd.to_datetime(r.index)
    return r

def load_factor_returns_csv(path: str, date_col: str = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = _to_datetime_index(df, date_col=date_col)
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(how="all")
    return df

def align_and_clean(stock_ret: pd.Series, factor_rets: pd.DataFrame, rf_col: str = None) -> tuple[pd.Series, pd.DataFrame]:
    df = pd.concat([stock_ret, factor_rets], axis=1, join="inner").dropna()
    y = df["stock_ret"].astype(float)

    X = df.drop(columns=["stock_ret"])
    if rf_col and rf_col in X.columns:
        y = y - X[rf_col].astype(float)
        X = X.drop(columns=[rf_col])

    return y, X

def ols_with_intercept(y: np.ndarray, X: np.ndarray) -> tuple[float, np.ndarray, float]:
    n = y.shape[0]
    X1 = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    yhat = X1 @ beta
    ssr = np.sum((y - yhat) ** 2)
    sst = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - (ssr / sst if sst > 0 else np.nan)
    alpha = float(beta[0])
    betas = beta[1:]
    return alpha, betas, float(r2)

def compute_factor_vector(
    stock_ret: pd.Series,
    factor_rets: pd.DataFrame,
    rf_col: str = None
) -> FactorResult:
    y_s, X_df = align_and_clean(stock_ret, factor_rets, rf_col=rf_col)
    y = y_s.to_numpy(dtype=float)
    X = X_df.to_numpy(dtype=float)

    alpha, betas, r2 = ols_with_intercept(y, X)
    beta_s = pd.Series(betas, index=X_df.columns, name="beta")

    return FactorResult(
        alpha_daily=alpha,
        betas=beta_s,
        r2=r2,
        nobs=int(len(y))
    )

def annualize_alpha(alpha_daily: float, periods_per_year: int = 252) -> float:
    return (1.0 + alpha_daily) ** periods_per_year - 1.0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", type=str, default=None)
    p.add_argument("--start", type=str, default="2020-01-01")
    p.add_argument("--end", type=str, default=None)

    p.add_argument("--stock-csv", type=str, default=None)
    p.add_argument("--stock-date-col", type=str, default=None)
    p.add_argument("--stock-price-col", type=str, default=None)
    p.add_argument("--stock-ret-col", type=str, default=None)

    p.add_argument("--factors-csv", type=str, required=True)
    p.add_argument("--factors-date-col", type=str, default=None)
    p.add_argument("--rf-col", type=str, default=None)

    args = p.parse_args()

    if args.end is None:
        args.end = pd.Timestamp.today().strftime("%Y-%m-%d")

    if args.stock_csv:
        stock_ret = load_stock_returns_from_csv(
            args.stock_csv,
            date_col=args.stock_date_col,
            price_col=args.stock_price_col,
            ret_col=args.stock_ret_col
        )
    elif args.ticker:
        stock_ret = try_load_stock_returns_yfinance(args.ticker, args.start, args.end)
    else:
        raise SystemExit("Provide --stock-csv or --ticker.")

    factor_rets = load_factor_returns_csv(args.factors_csv, date_col=args.factors_date_col)

    res = compute_factor_vector(stock_ret, factor_rets, rf_col=args.rf_col)

    alpha_ann = annualize_alpha(res.alpha_daily)

    out = pd.concat([pd.Series({"alpha_daily": res.alpha_daily, "alpha_annualized": alpha_ann, "r2": res.r2, "nobs": res.nobs}), res.betas])
    out.index = out.index.astype(str)
    print(out.to_string(float_format=lambda x: f"{x: .6f}"))

if __name__ == "__main__":
    main()
