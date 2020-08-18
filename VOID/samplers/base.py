import numpy as np

from VOID.object import ParseableObject


class Sampler(ParseableObject):
    def __init__(self):
        pass

    def get_points(self, structure):
        raise NotImplementedError


class OriginSampler(Sampler):
    PARSER_NAME = "origin"
    HELP = "Samples the origin of the structure"

    def __init__(self):
        super().__init__()

    def get_points(self, structure):
        return [np.array([0, 0, 0])]
