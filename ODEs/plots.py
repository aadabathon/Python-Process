import numpy as np
import matplotlib.pyplot as plt

def euler(f, x0, y0, h, n):
    x = np.zeros(n)
    y = np.zeros(n)
    x[0], y[0] = x0, y0
    for i in range(1, n):
        y[i] = y[i-1] + h * f(x[i-1], y[i-1])
        x[i] = x[i-1] + h
    return x, y

def plot_direction_field(f, xlim, ylim, density=20):
    x = np.linspace(xlim[0], xlim[1], density)
    y = np.linspace(ylim[0], ylim[1], density)
    X, Y = np.meshgrid(x, y)

    U = np.ones_like(X)
    V = f(X, Y)

    N = np.sqrt(U**2 + V**2)
    U, V = U/N, V/N

    plt.quiver(X, Y, U, V)
    plt.xlabel("x")
    plt.ylabel("y")

def example():
    f = lambda x, y: x  # dy/dx = x

    plot_direction_field(f, (-5, 12), (-5, 55))

    for y0 in [-6, -3, 0, 3, 6]:
        x, y = euler(f, 0, y0, 0.05, 200)
        plt.plot(x, y)

    plt.title("dy/dx = x")
    plt.show()

if __name__ == "__main__":
    example()
