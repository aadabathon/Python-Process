
def KellyCriterion(p, q, g, l, Bankroll):
    optimum = p/l - q/g
    print(f"R on this trade is optimal at {optimum * Bankroll}")


p = .625
q = 1 - p
g = .6
l = 1
Bankroll = 4300

KellyCriterion(p, q, g, l, Bankroll)