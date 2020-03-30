import numpy as np
from tqdm import tqdm
from sklearn.cluster import KMeans

from docking.zeolite import voronoi 
import docking.zeolite.utils as zeoutils


CLEARANCE = 1.0
DEFAULT_ATTEMPTS = 100
VORONOI_POINTS = 10
BEST_STRUCTURES = 10
MAX_LOADING = True


class Docker:
    def __init__(
        self,
        substrate,
        molecule,
        clearance=CLEARANCE,
        **kwargs
    ):
        self.substrate = substrate.copy()
        self.molecule = molecule.copy().get_centered_molecule()
        self.substrate.DISTANCE_TOLERANCE = clearance

    def rotate_molecule(self, theta=None, axis=None):
        molecule = self.molecule.copy()

        if theta is None:
            theta = 2 * np.pi * np.random.rand(1)[0]

        if axis is None:
            axis = np.random.rand(3)

        molecule.rotate_sites(theta=theta, axis=axis)
        return molecule

    def translate_substrate(self, coords):
        """Translates all nodes of the substrate to the given coords.

        Args:
            coords (np.array): (3, ) array with cartesian coordinates.
        """

        substrate = self.substrate.copy()
        substrate.DISTANCE_TOLERANCE = self.substrate.DISTANCE_TOLERANCE
        substrate.translate_sites(
            range(len(self.substrate)),
            -coords,
            frac_coords=False
        )

        return substrate

    def get_docking_points(self):
        raise NotImplementedError

    def dock(self, attempts=DEFAULT_ATTEMPTS, maximize_loading=MAX_LOADING):
        """Docks the molecule into the substrate.
        """

        docking_points = self.get_docking_points()
        docked_structures = []

        for point in tqdm(
            docking_points,
            'testing docking points'
        ):
            for idx in tqdm(range(attempts), 'attempts'):
                mol = self.rotate_molecule()
                subst = self.translate_substrate(point)

                try:
                    docked = zeoutils.join_structures(
                        mol,
                        subst,
                        validate_proximity=True
                    )
                    docked_structures.append(docked)

                except ValueError:
                    pass

        return docked_structures

    def copy(self, substrate=None, molecule=None):
        return self.__class__(
            self.substrate if substrate is None else substrate,
            self.molecule if molecule is None else molecule,
            clearance=self.substrate.DISTANCE_TOLERANCE
        )

    def increase_loading(self, structures, attempts=DEFAULT_ATTEMPTS):
        high_loading_structs = []
        for struct in tqdm(
            structures,
            'increasing the loading of the given structures'
        ):
            subdocker = self.copy(substrate=struct)
            subdocked_structs = subdocker.dock(attempts)
            high_loading_structs += subdocked_structs

        return high_loading_structs
    

