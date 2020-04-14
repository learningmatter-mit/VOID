import numpy as np

from .base import Fitness


THRESHOLD = 1.5


class ThresholdFitness(Fitness):
    def __init__(self, threshold=THRESHOLD, **kwargs):
        """Fitness is positive if the minimum distance is above
            the given threshold
        """
        super().__init__()
        self.threshold = threshold

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--threshold",
            type=float,
            help="threshold for distance calculations (default: %(default)s)",
            default=THRESHOLD,
        )


class MinDistanceFitness(ThresholdFitness):
    PARSER_NAME = "min_distance"
    HELP = "Complexes have positive score if the minimum distance between host and guest is above the given threshold"

    def __call__(self, complex):
        
        return complex.distance_matrix.min() - self.threshold


class MeanDistanceFitness(ThresholdFitness):
    PARSER_NAME = "mean_distance"
    HELP = "Complexes have positive score if the mean distance between host and guest is above the given threshold"

    def __call__(self, complex, axis=1):
        return complex.distance_matrix.min(axis=axis).mean() - self.threshold
