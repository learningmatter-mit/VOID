import numpy as np

from .base import Fitness


THRESHOLD = 1.5
DEFAULT_STRUCTURE = "complex"
STRUCTURE_CHOICES = ["complex", "guest", "host"]
DEFAULT_STEP = False


class ThresholdFitness(Fitness):
    def __init__(self, threshold=THRESHOLD, structure="complex", step=False, **kwargs):
        """Fitness is positive if the minimum distance is above
            the given threshold.

        Args:
            threshold (float)
            structure (str): defines to which structure the threshold will
                be applied. Can be either complex, guest or host.
        """
        super().__init__()
        self.threshold = threshold
        self.step = step

        if structure not in STRUCTURE_CHOICES:
            raise ValueError(
                "structure has to be one of: {}".format(", ".join(STRUCTURE_CHOICES))
            )
        self.structure = structure

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--threshold",
            type=float,
            help="threshold for distance calculations (default: %(default)s)",
            default=THRESHOLD,
        )
        parser.add_argument(
            "--structure",
            type=str,
            choices=STRUCTURE_CHOICES,
            help="threshold for distance calculations (default: %(default)s)",
            default=DEFAULT_STRUCTURE,
        )

    def get_distances(self, complex):
        if self.structure == "complex":
            return complex.distance_matrix

        elif self.structure == "host":
            idx = np.triu_indices(len(complex.host), k=1)
            return complex.get_distance_matrix("host")[idx]

        elif self.structure == "guest":
            idx = np.triu_indices(len(complex.guest), k=1)
            return complex.get_distance_matrix("guest")[idx]

        else:
            raise ValueError("structure type not supported")

    def normalize(self, value):
        if self.step:
            return 0 if value > 0 else -1
        return value


class MinDistanceFitness(ThresholdFitness):
    PARSER_NAME = "min_distance"
    HELP = "Complexes have positive score if the minimum distance between host and guest is above the given threshold"

    def __call__(self, complex):
        return self.normalize(self.get_distances(complex).min() - self.threshold)


class MeanDistanceFitness(ThresholdFitness):
    PARSER_NAME = "mean_distance"
    HELP = "Complexes have positive score if the mean distance between host and guest is above the given threshold"

    def __call__(self, complex, axis=-1):
        return self.normalize(
            self.get_distances(complex).min(axis=axis).mean() - self.threshold
        )


class SumInvDistanceFitness(ThresholdFitness):
    PARSER_NAME = "sum_distance"
    HELP = "Complexes have positive score if the sum of distances is above the given threshold"

    def __call__(self, complex):
        distances = self.get_distances(complex)
        distances = distances[distances < 2 * self.threshold]

        return self.normalize(-np.mean(1 / distances))
