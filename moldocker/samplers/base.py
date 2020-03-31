import numpy as np


class Sampler:
    def __init__(self):
        pass

    def get_points(self, structure):
        raise NotImplementedError


class OriginSampler(Sampler):
    def __init__(self):
        super().__init__()

    def get_points(self, structure):
        return [np.array([0, 0, 0])]
