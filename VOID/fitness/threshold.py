import numpy as np
import argparse
from .base import Fitness

THRESHOLD = 1.5
THRESHOLD_CATAN = 3.5
DEFAULT_STRUCTURE = "complex"
STRUCTURE_CHOICES = ["complex", "guest", "host"]
DEFAULT_STEP = False
CATION_INDEXES = None
ACID_SITES = None


class ThresholdFitness(Fitness):
    def __init__(
        self,
        threshold=THRESHOLD,
        structure="complex",
        step=False,
        **kwargs,
    ):
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
        self.extra_args = kwargs

        if structure not in STRUCTURE_CHOICES:
            raise ValueError("structure has to be one of: {}".format(", ".join(STRUCTURE_CHOICES)))
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

    def get_cation_anion_distances(self, acid_sites, cation_indexes, distance_matrices):
        """Get the distances between the cation and the anion sites.

        Args:
            acid_sites (list): List of lists of anion indexes.
            cation_index (int): Index of the cation.
            distance_matrices (list): List of distance matrices.

        Returns:

            list: List of lists of distances between the cation and the anion sites.
        """

        distances_cation_anion = []
        for cation in cation_indexes:
            distances = [distance_matrices[cation][anion_index] for anion_list in acid_sites for anion_index in anion_list]
            distances_cation_anion.append(distances)
        return distances_cation_anion

    def normalize(self, value):
        if self.step:
            return 0 if value > 0 else -np.inf
        return value


class MinDistanceFitness(ThresholdFitness):
    PARSER_NAME = "min_distance"
    HELP = "Complexes have positive score if the minimum distance between host and guest is above the given threshold"

    def __call__(self, complex):
        return self.normalize(self.get_distances(complex).min() - self.threshold)


class MinDistanceCationAnionFitness(ThresholdFitness):
    PARSER_NAME = "min_catan_distance"
    HELP = "Complexes have positive score if the minimum distance between host anion and guest cation is below the given threshold plus Complexes have positive score if the minimum distance between host and guest is above the given threshold"

    def __init__(
        self,
        threshold=THRESHOLD,
        threshold_catan=THRESHOLD_CATAN,
        structure=DEFAULT_STRUCTURE,
        cation_indexes=None,
        acid_sites=None,
        **kwargs,
    ):
        super().__init__(threshold, structure, **kwargs)
        self.threshold_catan = threshold_catan
        self.cation_indexes = cation_indexes
        self.acid_sites = acid_sites

    @staticmethod
    def add_arguments(parser):
        ThresholdFitness.add_arguments(parser)

        parser.add_argument(
            "--threshold_catan",
            type=float,
            help="threshold for cation-anion distance calculations (default: %(default)s)",
            default=THRESHOLD_CATAN,
        )
        parser.add_argument(
            "--cation_indexes",
            type=lambda x: [int(i) for i in x.split(",")],
            help="indexes for the atoms holding a positive charge in the molecule (default: %(default)s)",
            default=CATION_INDEXES,
        )
        parser.add_argument(
            "--acid_sites",
            type=lambda x: [list(map(int, group.split(","))) for group in x.split(";")],
            help="list of indexes for the O atoms that hold a negative charge (default: %(default)s)",
            default=ACID_SITES,
        )

    def __call__(self, complex):
        """Docks a guest cation into a host with anionic spots while ensuring a minimal distance between them.

        Args:
            complex (structure): The host-guest complex object containing the host and guest molecules.

        Returns:
            float: The score of the docking process. Returns normalized minimum distance if the optimal cation-anion distance is found, otherwise returns negative infinity.
        """

        cation_anion_distances = self.get_cation_anion_distances(
            self.acid_sites,
            self.cation_indexes,
            complex.pose.distance_matrix,
        )

        if (
            any(distance < self.threshold_catan for distance_list in cation_anion_distances for distance in distance_list)
            and self.normalize(self.get_distances(complex).min() - self.threshold) > 0
        ):
            print("Optimal cation-anion distance found! Aborting the run")
            return self.normalize(self.get_distances(complex).min())

        else:
            return -np.inf


class MeanDistanceFitness(ThresholdFitness):
    PARSER_NAME = "mean_distance"
    HELP = "Complexes have positive score if the mean distance between host and guest is above the given threshold"

    def __call__(self, complex, axis=-1):
        return self.normalize(self.get_distances(complex).min(axis=axis).mean() - self.threshold)


class SumInvDistanceFitness(ThresholdFitness):
    PARSER_NAME = "sum_distance"
    HELP = "Complexes have positive score if the sum of distances is above the given threshold"

    def __call__(self, complex):
        distances = self.get_distances(complex)
        distances = distances[distances < 2 * self.threshold]

        return self.normalize(-np.mean(1 / distances))
