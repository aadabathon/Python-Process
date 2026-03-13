import math
import numpy as np
import matplotlib.pyplot as plt

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bs_call(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

def bs_put(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def simulate_terminal_prices(S0, r, sigma, T, n_paths, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.normal(0.0, 1.0, size=n_paths)
    drift = (r - 0.5 * sigma**2) * T
    diffusion = sigma * math.sqrt(T) * Z
    ST = S0 * np.exp(drift + diffusion)
    return ST

def mc_call_price(S0, K, T, r, sigma, n_paths, seed=0):
    ST = simulate_terminal_prices(S0, r, sigma, T, n_paths, seed=seed)
    payoff = np.maximum(ST - K, 0.0)
    return math.exp(-r * T) * payoff.mean()

def plot_ST_histogram_with_lognormal(S0, r, sigma, T, n_paths=100000, seed=0):
    ST = simulate_terminal_prices(S0, r, sigma, T, n_paths, seed=seed)
    plt.figure()
    plt.hist(ST, bins=80, density=True, alpha=0.6, label="Simulated $S_T$")
    mu = math.log(S0) + (r - 0.5 * sigma**2) * T
    sigT = sigma * math.sqrt(T)
    x = np.linspace(ST.min() * 0.8, ST.max() * 1.2, 500)
    pdf = (1.0 / (x * sigT * math.sqrt(2.0 * math.pi))) * np.exp(-(np.log(x) - mu)**2 / (2.0 * sigT**2))
    plt.plot(x, pdf, linewidth=2, label="Lognormal pdf")
    plt.xlabel("$S_T$")
    plt.ylabel("Density")
    plt.title("Distribution of $S_T$ (Monte Carlo vs Lognormal)")
    plt.legend()
    plt.grid(True)

def plot_mc_convergence(S0, K, T, r, sigma):
    Ns = np.array([100, 300, 1000, 3000, 10000, 30000, 100000])
    mc_prices = []
    for i, N in enumerate(Ns):
        price = mc_call_price(S0, K, T, r, sigma, N, seed=i)
        mc_prices.append(price)
    mc_prices = np.array(mc_prices)
    bs_price = bs_call(S0, K, T, r, sigma)

    plt.figure()
    plt.plot(Ns, mc_prices, marker="o", label="MC call price")
    plt.axhline(bs_price, linestyle="--", label=f"BS price = {bs_price:.4f}")
    plt.xscale("log")
    plt.xlabel("Number of paths (log scale)")
    plt.ylabel("Call price")
    plt.title("Monte Carlo Convergence to Black–Scholes Price")
    plt.legend()
    plt.grid(True)

def plot_call_put_vs_strike(S0, T, r, sigma):
    Ks = np.linspace(50, 150, 200)
    calls = np.array([bs_call(S0, K, T, r, sigma) for K in Ks])
    puts = np.array([bs_put(S0, K, T, r, sigma) for K in Ks])

    plt.figure()
    plt.plot(Ks, calls, label="Call price")
    plt.plot(Ks, puts, label="Put price")
    plt.xlabel("Strike K")
    plt.ylabel("Option price")
    plt.title("Black–Scholes Call and Put vs Strike")
    plt.legend()
    plt.grid(True)

def simulate_paths(S0, r, sigma, T, n_steps, n_paths, seed=0):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    drift = (r - 0.5 * sigma**2) * dt
    diff_coeff = sigma * math.sqrt(dt)
    S = np.zeros((n_steps + 1, n_paths))
    S[0, :] = S0
    for t in range(1, n_steps + 1):
        Z = rng.normal(0.0, 1.0, size=n_paths)
        S[t, :] = S[t - 1, :] * np.exp(drift + diff_coeff * Z)
    return S

def plot_sample_paths(S0, r, sigma, T, n_steps=252, n_paths=10, seed=0):
    S = simulate_paths(S0, r, sigma, T, n_steps, n_paths, seed)
    times = np.linspace(0.0, T, n_steps + 1)
    plt.figure()
    for i in range(n_paths):
        plt.plot(times, S[:, i])
    plt.xlabel("Time")
    plt.ylabel("Stock price")
    plt.title("Sample GBM Wealth Paths")
    plt.grid(True)



if __name__ == "__main__":
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.05
    sigma = 0.2

    print("Black–Scholes call:", bs_call(S0, K, T, r, sigma))
    print("Black–Scholes put :", bs_put(S0, K, T, r, sigma))

    plot_sample_paths(S0, r, sigma, T, n_steps=252, n_paths=150, seed=42)
    plot_ST_histogram_with_lognormal(S0, r, sigma, T, n_paths=100000, seed=1)
    plot_mc_convergence(S0, K, T, r, sigma)
    plot_call_put_vs_strike(S0, T, r, sigma)

    plt.show()
