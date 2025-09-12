import numpy as np
import argparse
from .base import Fitness
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import GetPeriodicTable
from pymatgen.core.periodic_table import Element

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

    @staticmethod
    def compute_acid_sites(complex):
        """Identify acid sites in the host molecule of the complex."""
        acid_sites = []
        host = complex.host  # host molecule
        distances = complex.get_distance_matrix("host")

        host_oxygens = [i for i, site in enumerate(host) if site.specie.symbol == "O"]
        host_aluminum = [i for i, site in enumerate(host) if site.specie.symbol == "Al"]

        for al_idx in host_aluminum:
            candidate_oxygens = [
                i for i in host_oxygens if 0 < distances[al_idx, i] < 1.9
            ]
            if len(candidate_oxygens) == 4 and all(
                all(not (dist < 1.10 and dist != 0.0) for dist in distances[ox])
                for ox in candidate_oxygens
            ):
                acid_sites.append(candidate_oxygens)

        #print('acid sites', acid_sites)
        return acid_sites


    @staticmethod
    def compute_cation_indexes(complex, scale_cutoff=1.2):
        """
        Identify likely cation atoms in the guest molecule heuristically:
        any atom that has one fewer bond than its typical neutral valence,
        using distances and covalent radii from pymatgen.
        
        scale_cutoff: float
            Factor to scale the sum of covalent radii to define a bond.
        """
    
        NEUTRAL_VALENCES = {
            "H": 1, "C": 4, "N": 3, "O": 2, "F": 1,
            "P": 3, "S": 2, "Cl": 1, "Br": 1, "I": 1, "Si": 4,
        }
    
        # Approximate bond orders based on distance ranges (Å)
        BOND_ORDER_VALUES = {
            "SINGLE": 1,
            "DOUBLE": 2,
            "TRIPLE": 3,
            "AROMATIC": 1.5,
        }
    
        guest_coords = np.array([site.coords for site in complex.guest])
        guest_elements = [site.specie.symbol for site in complex.guest]
        n_atoms = len(guest_coords)
    
        # Build connectivity and assign bond orders
        neighbor_map = {i: [] for i in range(n_atoms)}
        bond_order_map = {i: [] for i in range(n_atoms)}
    
        for i in range(n_atoms):
            for j in range(i + 1, n_atoms):
                dist = np.linalg.norm(guest_coords[i] - guest_coords[j])
                COVALENT_RADII = {
                    "H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
                    "P": 1.07, "S": 1.05, "Cl": 1.02, "Br": 1.20, "I": 1.39, "Si": 1.11,
                }
                r1 = COVALENT_RADII.get(guest_elements[i], 0.77)  # default ~C
                r2 = COVALENT_RADII.get(guest_elements[j], 0.77)
                cutoff = scale_cutoff * (r1 + r2)
                if dist <= cutoff:
                    # Assign bond order based on distance relative to typical covalent radii
                    if dist >= 1.15 and dist <= 1.25:
                        order = "TRIPLE"
                    elif dist >= 1.26 and dist <= 1.37:
                        order = "DOUBLE"
                    elif dist >=1.38 and dist <= 1.42:
                        order = "AROMATIC"
                    else:
                        order = "SINGLE"
                    
                    neighbor_map[i].append(j)
                    neighbor_map[j].append(i)
                    bond_order_map[i].append(order)
                    bond_order_map[j].append(order)
    
        # Identify undercoordinated atoms (likely cations)
        cation_indexes = []
        host_len = len(complex.host)
    
        for idx, elem in enumerate(guest_elements):
            max_valence = NEUTRAL_VALENCES.get(elem)
            if max_valence is None:
                continue
            current_valence = sum(BOND_ORDER_VALUES[bo] for bo in bond_order_map[idx])
            if (current_valence - (max_valence - 1)) == 0:
                cation_indexes.append(host_len + idx)
    
        #print("cation indexes (heuristic with distance-based bonds):", cation_indexes)
        return cation_indexes


        

    def __call__(self, complex):
        """Docks a guest cation into a host with anionic spots while ensuring a minimal distance between them.

        Args:
            complex (structure): The host-guest complex object containing the host and guest molecules.

        Returns:
            float: The score of the docking process. Returns normalized minimum distance if the optimal cation-anion distance is found, otherwise returns negative infinity.
        """

        # Use computed acid sites if none were provided
        acid_sites = self.acid_sites or self.compute_acid_sites(complex)
        
        # Use computed cation indexes if none were provided
        cation_indexes = self.cation_indexes or self.compute_cation_indexes(complex)

        cation_anion_distances = self.get_cation_anion_distances(
            acid_sites,
            cation_indexes,
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
