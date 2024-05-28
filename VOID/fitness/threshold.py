import numpy as np

from .base import Fitness

from pymatgen.core.sites import Site


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

    def get_zeolite_oxygens(self, pose):
        """Collect all the O atoms in the structure."""
        return [index for index, site in enumerate(pose) if site.species_string == "O"]

    def find_cation_index(self, pose, distance_matrices):
        """Identify the cation position in the guest."""
        for index, site in enumerate(pose):
            element = site.species_string
            if element == "C":
                bonds = sum(1 for dist in distance_matrices[index] if 0 < dist < 1.6)
                if bonds == 3:
                    return index
        return None

    def find_acid_sites(self, pose, distance_matrices, zeolite_oxygens):
        """Identify the acid sites in the zeolite."""
        acid_oxygens = []
        acid_al_indexes = []

        for index, site in enumerate(pose):
            if site.species_string == "Al":
                candidate_oxygens = [
                    dist_index
                    for dist_index, dist in enumerate(distance_matrices[index])
                    if 0 < dist < 1.8 and dist_index in zeolite_oxygens
                ]
                if len(candidate_oxygens) == 4 and all(
                    all(
                        not (bond_dist < 1.15 and bond_dist != 0.0)
                        for bond_dist in distance_matrices[ox_index]
                    )
                    for ox_index in candidate_oxygens
                ):  # 1.15 accounts for O-H bond
                    acid_oxygens.append(candidate_oxygens)
                    acid_al_indexes.append(index)

        return acid_oxygens, acid_al_indexes

    def get_catan_distances(self, acid_oxygens, cation_index, distance_matrices):
        """Check the cation-anion distances for the different acid sites in the zeolite."""
        distances_catan = []
        for acid_al in acid_oxygens:
            distances_cation_anion = [
                distance_matrices[cation_index][ox_index] for ox_index in acid_al
            ]
            print(
                "Distances between cation and acid oxygens are:", distances_cation_anion
            )
            distances_catan.append(distances_cation_anion)
            # if any(dist < 2.0 for dist in distances_cation_anion):
            #    print("Optimal distance found! Aborting the run")
            #    return True
        # return False

        return distances_catan

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
    HELP = "Complexes have positive score if the minimum distance between host anion and guest cation is above the given threshold"

    def __call__(self, complex):
        # print(complex.pose)
        pose = complex.pose
        distance_matrices = complex.pose.distance_matrix
        zeolite_oxygens = self.get_zeolite_oxygens(pose)
        cation_index = self.find_cation_index(
            pose,
            distance_matrices,
        )
        acid_sites, acid_al_indexes = self.find_acid_sites(
            pose, distance_matrices, zeolite_oxygens
        )
        return self.normalize(
            min(self.get_catan_distances(acid_sites, cation_index, distance_matrices))
            - self.threshold
        )


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
