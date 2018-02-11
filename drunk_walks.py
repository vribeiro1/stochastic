import random
import matplotlib.pyplot as plt

N = (0, 1)
E = (1, 0)
S = (0, -1)
W = (-1, 0)
NE = (1, 1)
SE = (1, -1)
SW = (-1, -1)
NW = (-1, 1)


class Drunk:
    CHOICES = [N, S, E, W, NE, SE, SW, NW]

    def __init__(self):
        self.xloc = 0.0
        self.yloc = 0.0
        self.path = [(self.xloc, self.yloc)]

    def move(self):
        incr = random.choice(self.CHOICES)

        self.xloc += incr[0]
        self.yloc += incr[1]
        self.path.append((self.xloc, self.yloc))


class DrunkStark(Drunk):
    CHOICES = [N, N, S, E, W, NE, NE, SE, SW, NW, NW]


def simulate(drunk_class, n_sims, n_steps):
    simulations = range(n_sims)
    steps = range(n_steps)

    drunks = []
    for simulation in simulations:
        new_drunk = drunk_class()
        for step in steps:
            new_drunk.move()

        drunks.append(new_drunk)

    return drunks


if __name__ == "__main__":
    n_sims = 100
    n_steps = 1000

    drunks = simulate(Drunk, n_sims, n_steps)
    drunk_starks = simulate(DrunkStark, n_sims, n_steps)

    plt.figure(1)
    for drunk in drunks:
        plt.scatter(*zip(*drunk.path), c=[i for i in range(len(drunk.path))])
    plt.colorbar()

    plt.figure(2)
    for drunk in drunk_starks:
        plt.scatter(*zip(*drunk.path), c=[i for i in range(len(drunk.path))])
    plt.colorbar()

    plt.show()
