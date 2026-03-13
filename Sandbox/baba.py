def mean(data):
    return sum(data) / len(data)

def population_std(data):
    mu = mean(data)
    squared_diffs = [(x - mu) ** 2 for x in data]
    return (sum(squared_diffs) / len(data)) ** 0.5

def sample_std(data):
    mu = mean(data)
    squared_diffs = [(x - mu) ** 2 for x in data]
    return (sum(squared_diffs) / (len(data) - 1)) ** 0.5

# Example stock returns
returns = [0.01, -0.002, 0.003, 0.004, -0.005, 0.002, -0.001]

print("Population Std Dev:", population_std(returns))
print("Sample Std Dev:", sample_std(returns))
