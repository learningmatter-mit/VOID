from .base import Fitness
from .threshold import MinDistanceFitness, MeanDistanceFitness
from .target import MinDistanceGaussianTarget, MeanDistanceGaussianTarget
from .union import MultipleFitness

__all__ = [
    MinDistanceFitness, MeanDistanceFitness,
    MinDistanceGaussianTarget, MeanDistanceGaussianTarget,
    MultipleFitness
]
