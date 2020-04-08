import numpy as np

from .base import Score


class ThresholdScore(Score):
    def __init__(self, threshold):
        """Score is positive if the minimum distance is above
            the given threshold
        """
        super().__init__()
        self.threshold = threshold

    def add_arguments(self, parser):
        parser.add_argument(
            "--threshold",
            type=float,
            help="threshold for distance calculations",
            required=True,
        )


class MinDistanceScore(ThresholdScore):
    PARSER_NAME = "min_distance"
    HELP = "Complexes have positive score if the minimum distance between host and guest is above the given threshold"

    def __call__(self, distance_matrix):
        return distance_matrix.min() - self.threshold


class MeanDistanceScore(ThresholdScore):
    PARSER_NAME = "mean_distance"
    HELP = "Complexes have positive score if the mean distance between host and guest is above the given threshold"

    def __call__(self, distance_matrix, axis=1):
        return distance_matrix.min(axis=axis).mean() - self.threshold
