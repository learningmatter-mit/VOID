from .base import Fitness
from .threshold import MinDistanceFitness, MeanDistanceFitness
from .target import MinDistanceGaussianTarget, MeanDistanceGaussianTarget

__all__ = [
    MinDistanceFitness, MeanDistanceFitness,
    MinDistanceGaussianTarget, MeanDistanceGaussianTarget,
]
