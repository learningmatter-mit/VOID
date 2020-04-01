import numpy as np

from .base import Score


class ThresholdScore(Score):
    def __init__(self, threshold):
        """Score is positive if the minimum distance is above
            the given threshold
        """
        super().__init__()
        self.threshold = threshold


class MinDistanceScore(ThresholdScore):
    def __call__(self, distance_matrix):
        return distance_matrix.min() - self.threshold


class MeanDistanceScore(ThresholdScore):
    def __call__(self, distance_matrix, axis=1):
        return distance_matrix.min(axis=axis).mean() - self.threshold
