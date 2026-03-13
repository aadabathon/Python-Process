import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def rk4_step(F, state, t, h):
    k1 = F(state, t)
    k2 = F(state + 0.5*h*k1, t + 0.5*h)
    k3 = F(state + 0.5*h*k2, t + 0.5*h)
    k4 = F(state + h*k3, t + h)
    return state + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def draw_vector_field(ax, U, xlim, ylim, density=20):
    xs = np.linspace(xlim[0], xlim[1], density)
    ys = np.linspace(ylim[0], ylim[1], density)
    X, Y = np.meshgrid(xs, ys)

    Vx, Vy = U(X, Y)

    S = np.sqrt(Vx**2 + Vy**2) + 1e-12
    Vx, Vy = Vx/S, Vy/S

    ax.quiver(X, Y, Vx, Vy, angles="xy", scale_units="xy", scale=1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

def main():
    xlim = (-10, 10)
    ylim = (-10, 10)
    h = 0.02

    # velocity field: dx/dt = u(x,y), dy/dt = v(x,y)
    # Example: a swirl + sink (looks cool)
    def U(x, y):
        vx = -y - 0.2*x
        vy =  x - 0.2*y
        return vx, vy

    def F(state, t):
        x, y = state
        vx, vy = U(x, y)
        return np.array([vx, vy], dtype=float)

    fig, ax = plt.subplots()
    draw_vector_field(ax, U, xlim, ylim, density=25)
    ax.set_title("Click to spawn a particle")

    particles = []
    trails = []
    dots = []

    def on_click(event):
        if event.inaxes != ax:
            return
        state = np.array([event.xdata, event.ydata], dtype=float)
        particles.append(state)

        (trail,) = ax.plot([state[0]], [state[1]])
        (dot,) = ax.plot([state[0]], [state[1]], marker="o")
        trails.append(trail)
        dots.append(dot)

    fig.canvas.mpl_connect("button_press_event", on_click)

    def update(frame):
        for i in range(len(particles)):
            particles[i] = rk4_step(F, particles[i], frame*h, h)

            xdata = np.append(trails[i].get_xdata(), particles[i][0])
            ydata = np.append(trails[i].get_ydata(), particles[i][1])

            trails[i].set_data(xdata, ydata)
            dots[i].set_data([particles[i][0]], [particles[i][1]])
        return trails + dots

    FuncAnimation(fig, update, interval=16, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
