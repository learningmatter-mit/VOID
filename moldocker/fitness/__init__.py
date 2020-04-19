from .base import Fitness
from .threshold import MinDistanceFitness, MeanDistanceFitness, SumInvDistanceFitness
from .target import MinDistanceGaussianTarget, MeanDistanceGaussianTarget
from .union import MultipleFitness

__all__ = [
    MinDistanceFitness,
    MeanDistanceFitness,
    SumInvDistanceFitness,
    MinDistanceGaussianTarget,
    MeanDistanceGaussianTarget,
    MultipleFitness,
]
