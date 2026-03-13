import numpy as np
import matplotlib.pyplot as plt

class CryptoSim:
    def __init__(self, name="GPTCoin"):
        self.name = name
        self.price = 100.0
        self.history = [self.price]
        self.step = 0

    def tick(self):
        # random walk price movement
        change = np.random.normal(0, 1.5)
        self.price = max(0.1, self.price + change)
        self.history.append(self.price)
        self.step += 1
        return self.price

    def plot(self):
        plt.figure(figsize=(8,4))
        plt.plot(self.history, linewidth=2)
        plt.title(f"{self.name} Price Simulation")
        plt.xlabel("Time Step")
        plt.ylabel("Price")
        plt.grid(True)
        plt.show()

    def info(self):
        return f"[{self.name}] step={self.step} price=${self.price:.2f}"

# ---------------------------
# Example usage:
# ---------------------------

sim = CryptoSim("AdamCoin")

for _ in range(1000):
    sim.tick()

print(sim.info())
sim.plot()
