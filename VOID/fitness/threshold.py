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

    def get_atomtypes_indexes(self, pose):
        """Collect all the atomtypes indexes in the structure

        Args:
            pose (structure): Structure object containing atomtype, xyz, and host/guest features

        Returns:
            atomtypes_indexes (dict): dictionary comprising information about each atomtype, its indexes and the "host"/"guest" nature
        """
        atomtypes_indexes = {}

        for index, site in enumerate(pose):
            atom_type = site.species_string
            feature = site.label  # labels the atomtype as host or guest
            if atom_type not in atomtypes_indexes:
                atomtypes_indexes[atom_type] = []
            atomtypes_indexes[atom_type].append((index, feature))

        return atomtypes_indexes

    def find_cation_index(self, distance_matrices, atomtypes_indexes):
        """Identify the cation position in the guest molecule. This function is intended for monocationic species.

        Args:
            distance_matrices (list): List of distance matrix lists for each atom with respect to all other atoms.
            atomtypes_indexes (dict): Dictionary comprising information about each atomtype, its indexes, and its "host"/"guest" nature.

        Raises:
            ValueError: If the code cannot find the cation on the guest molecule.

        Returns:
            int: Index corresponding to the carbon (C) or nitrogen (N) atom that hosts the positive charge on the molecule.
        """

        # First retrieves the indexes for each atomtype, more can be added if needed
        carbon_indexes = [
            idx for idx, lbl in atomtypes_indexes.get("C", []) if lbl == "guest"
        ]
        nitrogen_indexes = [
            idx for idx, lbl in atomtypes_indexes.get("N", []) if lbl == "guest"
        ]
        oxygen_indexes = [
            idx for idx, lbl in atomtypes_indexes.get("O", []) if lbl == "guest"
        ]
        hydrogen_indexes = [
            idx for idx, lbl in atomtypes_indexes.get("H", []) if lbl == "guest"
        ]

        # Checks the numbers of bonds for each C atom, takes into account double and triple bonds
        for carbon_index in carbon_indexes:
            bonds = 0
            # Check all the dsitances and bond types for C-H, C-C, C-N, C-O
            for i, dist in enumerate(distance_matrices[carbon_index]):
                if (
                    i in carbon_indexes
                    or i in hydrogen_indexes
                    or i in nitrogen_indexes
                    or i in oxygen_indexes
                ):
                    if 0 < dist < 1.15 and i in hydrogen_indexes:  # exp C-H dist 1.09 A
                        bonds += 1
                    elif (
                        1.5 < dist < 1.6 and i in carbon_indexes
                    ):  # exp C-C dist 1.55 A
                        bonds += 1
                    elif (
                        1.29 < dist < 1.39 and i in carbon_indexes
                    ):  # exp C=C dist 1.34 A
                        bonds += 2
                    elif (
                        1.15 < dist < 1.25 and i in carbon_indexes
                    ):  # exp C≡C dist 1.20 A
                        bonds += 3
                    elif (
                        1.38 < dist < 1.48 and i in nitrogen_indexes
                    ):  # exp C-N dist 1.43 A
                        bonds += 1
                    elif (
                        1.33 < dist < 1.43 and i in nitrogen_indexes
                    ):  # exp C=N dist 1.38 A
                        bonds += 2
                    elif (
                        1.11 < dist < 1.21 and i in nitrogen_indexes
                    ):  # exp C≡N dist 1.16 A
                        bonds += 3
                    elif (
                        1.38 < dist < 1.48 and i in oxygen_indexes
                    ):  # exp C-O dist 1.43 A
                        bonds += 1
                    elif (
                        1.18 < dist < 1.28 and i in oxygen_indexes
                    ):  # exp C=O dist 1.28 A
                        bonds += 2
                    elif (
                        1.08 < dist < 1.18 and i in oxygen_indexes
                    ):  # exp C≡O dist 1.18 A
                        bonds += 3

            # If a C atom has only 3 bonds, identifies this atom as the positive charge holder
            if bonds == 3:
                return carbon_index

        # Checks the numbers of bonds for each N atom, takes into account double and triple bonds
        for nitrogen_index in nitrogen_indexes:
            bonds = 0
            # Checks all distances and bond types for N-H, N-C, N-N and N-O
            for i, dist in enumerate(distance_matrices[nitrogen_index]):
                if (
                    i in carbon_indexes
                    or i in hydrogen_indexes
                    or i in nitrogen_indexes
                    or i in oxygen_indexes
                ):
                    if 0 < dist < 1.05 and i in hydrogen_indexes:  # exp N-H dist 1.00 A
                        bonds += 1
                    elif (
                        1.42 < dist < 1.52 and i in carbon_indexes
                    ):  # exp N-N dist 1.47 A
                        bonds += 1
                    elif (
                        1.19 < dist < 1.29 and i in carbon_indexes
                    ):  # exp N=N dist 1.24 A
                        bonds += 2
                    elif (
                        1.05 < dist < 1.15 and i in carbon_indexes
                    ):  # exp N≡N dist 1.10 A
                        bonds += 3
                    elif (
                        1.38 < dist < 1.48 and i in nitrogen_indexes
                    ):  # exp C-N dist 1.43 A
                        bonds += 1
                    elif (
                        1.33 < dist < 1.43 and i in nitrogen_indexes
                    ):  # exp C=N dist 1.38 A
                        bonds += 2
                    elif (
                        1.11 < dist < 1.21 and i in nitrogen_indexes
                    ):  # exp C≡N dist 1.16 A
                        bonds += 3
                    elif (
                        1.39 < dist < 1.49 and i in oxygen_indexes
                    ):  # exp N-O dist 1.44 A
                        bonds += 1
                    elif (
                        1.15 < dist < 1.25 and i in oxygen_indexes
                    ):  # exp C=O dist 1.20 A
                        bonds += 2

            if bonds == 4:
                return nitrogen_index

        # If no cation index is found, raise an error with a custom message
        raise ValueError(
            "Cation index could not be found. Please check the molecule you are docking."
        )

    def find_acid_sites(self, distance_matrices, atomtypes_indexes):
        """Identify the acid sites in the host structure.

        Args:
            distance_matrices (list): List of distance matrix lists for each atom with respect to all other atoms.
            atomtypes_indexes (dict): Dictionary containing information about each atomtype, its indexes, and its "host"/"guest" nature.

        Returns:
            list: List of lists with 4 oxygen atom indexes attached to each acid site. These oxygen atoms account for the negative charge to be compensated by the cation.
            list: List of aluminum (Al) indexes, whose bonded oxygens are not compensated by any proton. (Not used throughout the code at present.)
        """

        acid_oxygens = []
        acid_al_indexes = []

        host_oxygens = [
            idx for idx, lbl in atomtypes_indexes.get("O", []) if lbl == "host"
        ]
        host_aluminum = [
            idx for idx, lbl in atomtypes_indexes.get("Al", []) if lbl == "host"
        ]
        ## Room to add more metals if needed for docking to metal slides or so

        # Checks every Al atom present on the host structure
        for al_index in host_aluminum:
            # gets the 4 closest atoms to it (hence the bonded ones), Al-O dist ~1.79
            candidate_oxygens = [
                dist_index
                for dist_index, dist in enumerate(distance_matrices[al_index])
                if 0 < dist < 1.9 and dist_index in host_oxygens
            ]
            # if there are 4 bonds and any of the 4 oxygens has an H bonded to it
            # Then the 4 oxygens are considered acid sites and can form a bond with the cation
            if len(candidate_oxygens) == 4 and all(
                all(
                    not (bond_dist < 1.10 and bond_dist != 0.0)
                    for bond_dist in distance_matrices[ox_index]
                )
                for ox_index in candidate_oxygens
            ):  # 1.10 accounts for O-H bond
                acid_oxygens.append(candidate_oxygens)
                acid_al_indexes.append(al_index)

        return acid_oxygens, acid_al_indexes

    def get_catan_distances(
        self, acid_oxygens, cation_index, distance_matrices, complex
    ):
        """Check the distances between the cation and anion for different acid sites in the zeolite.

        Args:
            acid_oxygens (list): List of lists with 4 oxygen atom indexes attached to each acid site; these oxygen atoms account for the negative charge to be compensated by the cation.
            cation_index (int): Index corresponding to the carbon (C) or nitrogen (N) atom that hosts the positive charge on the molecule.
            distance_matrices (list): List of distance matrix lists for each atom with respect to all other atoms.
            complex (structure): Structure object representing the host-guest complex.

        Returns:
            bool: True if both requirements are met; False if either of the requirements isn't met.
            list: List of distance lists between the cation index and the 4 acid oxygens corresponding to each acid Al.
        """

        distances_catan = []
        for acid_al in acid_oxygens:
            distances_cation_anion = [
                distance_matrices[cation_index][ox_index] for ox_index in acid_al
            ]

            distances_catan.append(distances_cation_anion)

        if (
            any(dist < 2.0 for sublist in distances_catan for dist in sublist)
            and self.normalize(self.get_distances(complex).min() - self.threshold) > 0
        ):
            print("Optimal distance found! Aborting the run")
            print(
                "Distances between cation and acid oxygens are:",
                distances_catan,
            )
            return True, distances_catan

        else:
            return False, distances_catan

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

    def __call__(self, complex):
        """Docks a guest cation into a host with anionic spots while ensuring a minimal distance between them.

        Args:
            complex (structure): The host-guest complex object containing the host and guest molecules.

        Returns:
            int: 1 if both MinDistanceFitness and MinDistanceCationAnionFitness criteria are met.
            float: Negative infinity (-np.inf) if either MinDistanceFitness or MinDistanceCationAnionFitness criteria are not met.
        """

        pose = complex.pose
        distance_matrices = complex.pose.distance_matrix
        atomtypes_indexes = self.get_atomtypes_indexes(pose)

        cation_index = self.find_cation_index(distance_matrices, atomtypes_indexes)
        acid_sites, acid_al_indexes = self.find_acid_sites(
            distance_matrices, atomtypes_indexes
        )

        converged, distances = self.get_catan_distances(
            acid_sites, cation_index, distance_matrices, complex
        )

        if converged:
            return 1

        else:
            return -np.inf


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
