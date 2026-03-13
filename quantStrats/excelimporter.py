# ---- Financials → Excel (Income, Balance, Cash Flow, FCF) ----
# pip install yfinance pandas openpyxl

import pandas as pd
import yfinance as yf
from pathlib import Path

# ------------ Helpers ------------
def _transpose_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    yfinance financials come with line-items as rows and columns as periods.
    Transpose so each row = period, columns = line items. Sort by date ascending.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.T.copy()
    # Normalize index to date strings for Excel
    out.index = pd.to_datetime(out.index).date
    out.sort_index(inplace=True)
    return out

def _pick(series_df: pd.DataFrame, candidates):
    """Return the first matching line-item Series by name from yfinance cashflow table."""
    for key in candidates:
        if key in series_df.index:
            return series_df.loc[key]
    return None

def _compute_fcf(cashflow_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Free Cash Flow = Operating Cash Flow + Capital Expenditures (Yahoo capex is negative).
    Returns a tidy DataFrame with Operating CF, CapEx, FCF.
    """
    if cashflow_df is None or cashflow_df.empty:
        return pd.DataFrame()

    # work in original orientation (rows=line items), so select by index:
    cf = cashflow_df.copy()

    op_cf = _pick(cf, ["Operating Cash Flow", "Total Cash From Operating Activities"])
    capex = _pick(cf, ["Capital Expenditures", "Capital Expenditure"])

    if op_cf is None or capex is None:
        return pd.DataFrame()

    # Build tidy, transpose to rows=periods
    fcf = pd.DataFrame({
        "Operating Cash Flow": op_cf,
        "Capital Expenditures": capex
    })
    fcf["Free Cash Flow"] = fcf["Operating Cash Flow"] + fcf["Capital Expenditures"]  # capex is negative on Yahoo
    fcf = fcf.sort_index()
    fcf.index = pd.to_datetime(fcf.index).date
    return fcf

def fetch_statements(ticker: str):
    """
    Pulls annual & quarterly: income, balance, cashflow + FCF (derived).
    Returns dict of tidy DataFrames (rows=period, cols=line items).
    """
    t = yf.Ticker(ticker)
    fin_a  = t.financials            # income (annual)
    fin_q  = t.quarterly_financials  # income (quarterly)
    bs_a   = t.balance_sheet
    bs_q   = t.quarterly_balance_sheet
    cf_a   = t.cashflow
    cf_q   = t.quarterly_cashflow

    out = {
        "Income_Annual":     _transpose_clean(fin_a),
        "Income_Quarterly":  _transpose_clean(fin_q),
        "Balance_Annual":    _transpose_clean(bs_a),
        "Balance_Quarterly": _transpose_clean(bs_q),
        "Cashflow_Annual":   _transpose_clean(cf_a),
        "Cashflow_Quarterly":_transpose_clean(cf_q),
        "FCF_Annual":        _compute_fcf(cf_a),
        "FCF_Quarterly":     _compute_fcf(cf_q),
    }
    return out

def write_excel(tickers, xlsx_path="company_financials.xlsx"):
    """
    Writes all statements for all tickers into one Excel file, with clear sheet names.
    Also creates 'Summary_FCF_Annual' & 'Summary_FCF_Quarterly' for quick scanning.
    """
    xlsx_path = Path(xlsx_path)
    summary_fcf_a = {}
    summary_fcf_q = {}

    with pd.ExcelWriter(xlsx_path, engine="openpyxl", datetime_format="YYYY-MM-DD") as writer:
        for tk in tickers:
            print(f"Fetching {tk} …")
            data = fetch_statements(tk)

            for key, df in data.items():
                if df is None or df.empty:
                    print(f"  - {tk}:{key} empty (not available).")
                    continue

                sheet = f"{tk}_{key}"
                # Excel sheet name max length = 31
                if len(sheet) > 31:
                    sheet = sheet[:31]
                df.to_excel(writer, sheet_name=sheet)
                print(f"  ✓ wrote {sheet}")

            # collect FCF summaries
            if data["FCF_Annual"] is not None and not data["FCF_Annual"].empty:
                summary_fcf_a[tk] = data["FCF_Annual"]["Free Cash Flow"]
            if data["FCF_Quarterly"] is not None and not data["FCF_Quarterly"].empty:
                summary_fcf_q[tk] = data["FCF_Quarterly"]["Free Cash Flow"]

        # Write summaries as wide tables (index=Period, columns=Tickers)
        if summary_fcf_a:
            fcf_a = pd.DataFrame(summary_fcf_a).sort_index()
            fcf_a.to_excel(writer, sheet_name="Summary_FCF_Annual")
            print("  ✓ wrote Summary_FCF_Annual")
        if summary_fcf_q:
            fcf_q = pd.DataFrame(summary_fcf_q).sort_index()
            fcf_q.to_excel(writer, sheet_name="Summary_FCF_Quarterly")
            print("  ✓ wrote Summary_FCF_Quarterly")

    print(f"\nDone → {xlsx_path.resolve()}")

# ------------ Run it ------------
# Edit this list to whatever tickers you want:
tickers = ["AAPL", "MSFT", "GOOGL"]  # add more tickers here
write_excel(tickers, xlsx_path="company_financials.xlsx")
