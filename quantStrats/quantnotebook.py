import math
import numpy as np
import matplotlib.pyplot as plt

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def black_scholes_call(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

def black_scholes_put(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

if __name__ == "__main__":
    S0 = 100.0   # underlying price
    T = 1.0      # time to maturity in years
    r = 0.05     # risk-free rate
    sigma = 0.2  # volatility

    Ks = np.linspace(50, 150, 200)

    calls = [black_scholes_call(S0, K, T, r, sigma) for K in Ks]
    puts = [black_scholes_put(S0, K, T, r, sigma) for K in Ks]

    plt.figure()
    plt.plot(Ks, calls, label="Call price")
    plt.plot(Ks, puts, label="Put price")
    plt.xlabel("Strike K")
    plt.ylabel("Option price")
    plt.title("Black–Scholes Call vs Put Prices (S fixed at {:.0f})".format(S0))
    plt.legend()
    plt.grid(True)
    plt.show()
