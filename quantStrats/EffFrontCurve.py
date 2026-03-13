import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def portfolio_stats(weights, mu, cov):
    ret = np.dot(weights, mu)
    vol = np.sqrt(weights.T @ cov @ weights)
    return ret, vol

def minimize_vol(target_return, mu, cov):
    n = len(mu)
    def obj(w):
        return np.sqrt(w.T @ cov @ w)
    cons = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        {"type": "eq", "fun": lambda w: np.dot(w, mu) - target_return},
    )
    bounds = [(0.0, 1.0)] * n
    w0 = np.ones(n) / n
    res = minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=cons)
    return res

def efficient_frontier(mu, cov, num_points=100):
    mu = np.array(mu)
    cov = np.array(cov)
    target_returns = np.linspace(mu.min(), mu.max(), num_points)
    vols = []
    rets = []
    weights = []
    for tr in target_returns:
        res = minimize_vol(tr, mu, cov)
        if not res.success:
            continue
        w = res.x
        r, v = portfolio_stats(w, mu, cov)
        rets.append(r)
        vols.append(v)
        weights.append(w)
    return np.array(vols), np.array(rets), np.array(weights)

def make_sample_prices():
    np.random.seed(0)
    n_days = 252 * 3
    tickers = ["ASSET_A", "ASSET_B", "ASSET_C", "ASSET_D"]
    dates = pd.date_range("2020-01-01", periods=n_days, freq="B")

    mu_daily = np.array([0.12, 0.08, 0.15, 0.05]) / 252
    sigma_daily = np.array([0.20, 0.15, 0.25, 0.10]) / np.sqrt(252)
    corr = np.array([
        [1.0, 0.6, 0.3, 0.2],
        [0.6, 1.0, 0.4, 0.3],
        [0.3, 0.4, 1.0, 0.1],
        [0.2, 0.3, 0.1, 1.0],
    ])
    cov_daily = np.outer(sigma_daily, sigma_daily) * corr
    L = np.linalg.cholesky(cov_daily)
    z = np.random.randn(n_days, len(tickers))
    rand_returns = z @ L.T + mu_daily
    prices = 100 * np.exp(np.cumsum(rand_returns, axis=0))

    df = pd.DataFrame(prices, index=dates, columns=tickers)
    return df

def main():
    print("Generating sample prices...")
    df = make_sample_prices()
    returns = df.pct_change().dropna()

    mu = returns.mean() * 252
    cov = returns.cov() * 252

    print("Computing efficient frontier...")
    vols, rets, _ = efficient_frontier(mu.values, cov.values, num_points=100)

    print("Plotting...")
    plt.figure()
    plt.plot(vols, rets)
    plt.xlabel("Volatility (Std Dev)")
    plt.ylabel("Expected Return")
    plt.title("Efficient Frontier (Sample Data)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    input("Done. Press Enter to exit...")

if __name__ == "__main__":
    main()

