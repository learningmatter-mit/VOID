import numpy as np

from .base import Fitness


TARGET = 1.5
TOLERANCE = 0.2


class TargetFitness(Fitness):
    """Fitness function that optimizes a target property"""

    def __init__(self, target=TARGET, tolerance=TOLERANCE):
        """
        Args:
            target (float): target value for the property
            tolerance (float): width of the region with
                acceptable values for the property. Equivalent
                to a standard deviation accepted for property
                variation
        """
        super().__init__()
        self.target = target
        self.tolerance = tolerance

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--target",
            type=float,
            help="target for property optimization (default: %(default)s)",
            default=TARGET,
        )
        parser.add_argument(
            "--tolerance",
            type=float,
            help="tolerance for property optimization (default: %(default)s)",
            default=TOLERANCE,
        )


class GaussianTargetFitness(TargetFitness):
    def metric(self, x):
        return np.exp(-np.power(x, 2.0) / (2 * np.power(self.tolerance, 2.0)))


class MinDistanceGaussianTarget(GaussianTargetFitness):
    PARSER_NAME = "min_distance_target"
    HELP = "Complexes have higher score if the minimum distance between host and guest is close to the given target"

    def __call__(self, complex):
        return self.metric(complex.distance_matrix.min() - self.target)


class MeanDistanceGaussianTarget(GaussianTargetFitness):
    PARSER_NAME = "mean_distance_target"
    HELP = "Complexes have higher score if the mean distance between host and guest is close to the given target"

    def __call__(self, complex, axis=1):
        return self.metric(complex.distance_matrix.min(axis=axis).mean() - self.target)
