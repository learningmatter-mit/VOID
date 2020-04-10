import numpy as np

from .base import Sampler


SAMPLES = 10

class RandomSampler(Sampler):
    PARSER_NAME = "random"
    HELP = "Sample random points inside the unit cell of the given crystal structure"
    def __init__(self, num_samples=SAMPLES, **kwargs):
        self.num_samples = num_samples

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--num_samples",
            type=int,
            help="maximum number of points inside the crystal structure to sample (default: %(default)s)",
            default=SAMPLES,
        )

    def get_points(self, structure):
        points = np.random.rand(self.num_samples, 3)
        return points @ structure.lattice.matrix

