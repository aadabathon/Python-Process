import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def pick_returns_column(df, col_hint=None):
    if col_hint and col_hint in df.columns:
        s = pd.to_numeric(df[col_hint], errors="coerce")
        return col_hint, s

    num_cols = []
    for c in df.columns:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() >= max(20, int(0.2 * len(df))):
            num_cols.append((c, s.notna().sum()))
    if not num_cols:
        raise ValueError("No usable numeric column found. Pass --col with your returns column name.")
    num_cols.sort(key=lambda x: x[1], reverse=True)
    c = num_cols[0][0]
    return c, pd.to_numeric(df[c], errors="coerce")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--col", default=None)
    ap.add_argument("--out", default="returns_dist.png")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--percent", action="store_true")
    args = ap.parse_args()

    df = pd.read_csv(args.csv_path)
    col, r = pick_returns_column(df, args.col)
    r = r.dropna().astype(float).to_numpy()
    if r.size == 0:
        raise ValueError("Returns column has no numeric values after cleaning.")

    scale = 100.0 if args.percent else 1.0
    r_plot = r * scale
    unit = "%" if args.percent else ""

    n = r_plot.size
    r_sorted = np.sort(r_plot)
    ecdf = np.arange(1, n + 1) / n

    rng = np.random.default_rng(args.seed)
    jitter = rng.uniform(-0.35, 0.35, size=n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    ax1.plot(r_sorted, ecdf)
    ax1.set_title(f"ECDF (each return counts once) — {col}")
    ax1.set_xlabel(f"Return{unit}")
    ax1.set_ylabel("Cumulative probability")
    ax1.grid(True, alpha=0.25)

    ax2.scatter(jitter, r_plot, s=12, alpha=0.5)
    ax2.axhline(0, linewidth=1)
    mean = float(np.mean(r_plot))
    med = float(np.median(r_plot))
    ax2.scatter([0], [mean], s=80, marker="D", label=f"mean = {mean:.4g}{unit}")
    ax2.scatter([0], [med], s=80, marker="s", label=f"median = {med:.4g}{unit}")
    ax2.set_title("Dot distribution (every single return plotted)")
    ax2.set_xlabel("jitter (no meaning)")
    ax2.set_ylabel(f"Return{unit}")
    ax2.set_xlim(-0.5, 0.5)
    ax2.grid(True, axis="y", alpha=0.25)
    ax2.legend()

    fig.suptitle(f"Returns distribution from {args.csv_path}", fontsize=12)
    plt.savefig(args.out, dpi=200)
    plt.show()

    q = np.quantile(r_plot, [0.01, 0.05, 0.5, 0.95, 0.99])
    print(f"Column: {col}")
    print(f"n={n}")
    print(f"mean={mean:.6g}{unit}  median={med:.6g}{unit}  std={np.std(r_plot, ddof=1):.6g}{unit}")
    print(f"p01={q[0]:.6g}{unit}  p05={q[1]:.6g}{unit}  p50={q[2]:.6g}{unit}  p95={q[3]:.6g}{unit}  p99={q[4]:.6g}{unit}")
    print(f"Saved: {args.out}")

if __name__ == "__main__":
    main()
