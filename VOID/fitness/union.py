from .base import Fitness


class MultipleFitness(Fitness):
    def __init__(self, fitness, weights=None):
        self.fitness = fitness
        self.weights = [1] * len(fitness) if weights is None else weights

    def __call__(self, obj):
        return sum([w * f(obj) for w, f in zip(self.weights, self.fitness)])
