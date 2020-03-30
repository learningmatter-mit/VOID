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
    

class VoronoiDocker(Docker):
    def __init__(
        self,
        *args,
        probe_radius=voronoi.PROBE_RADIUS,
        remove_oxygen=voronoi.REMOVE_OXYGEN,
        min_radius=voronoi.MIN_VORONOI_RADIUS,
        num_voronoi_points=VORONOI_POINTS,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        voronoi_nodes_creator = voronoi.VoronoiNodes(
            probe_radius=probe_radius,
            remove_oxygen=remove_oxygen
        )
        self.nodes = voronoi_nodes_creator(
            self.substrate,
            min_radius=min_radius
        )
        self.num_voronoi_points = num_voronoi_points

    def get_docking_points(self):
        """Select best sites according to a k-means clustering
            algorithm. It provides us with a better selection of
            which points to try in the zeolite. Periodic boundary
            conditions are NOT taken into consideration when
            calculating the distances. The best sites are those
            further away from the zeolite (largest voronoi radius).
        """

        def cluster_points(X):
            n_clusters = min(len(X), self.num_voronoi_points)
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(X)
            return kmeans.labels_

        def select_sites(sites, labels):
            best_sites = []
            for i in range(self.num_voronoi_points):
                sites_cluster = [
                    site
                    for site, cluster in zip(sites, labels)
                    if cluster == i
                ]

                if len(sites_cluster) > 0:
                    best_site = max(
                        sites_cluster,
                        key=lambda site: site.properties['voronoi_radius'],
                    )

                    best_sites.append(best_site)

            return best_sites

        if len(self.nodes.cart_coords) == 0:
            return []
        
        clusters = cluster_points(self.nodes.cart_coords)
        best_sites = select_sites(self.nodes.sites, clusters)

        if len(best_sites) == 0:
            return []
        return [site.coords for site in best_sites]

    def select_best_structures(self, structures, n=BEST_STRUCTURES):
        """Select the best structures from the given list
            based on the goodness of fit of the molecule
            inside the pore.

        Args:
            structures (list of Structure)
            n (int): number of structures to select
        """
        fitness = [
            zeoutils.get_molecule_structure_distances(
                struct, len(self.substrate)
            )
            for struct in structures
        ]

        best_structures = [
            st 
            for st, _ in sorted(zip(structures, fitness), key=lambda x: x[1], reverse=True)
        ]

        return best_structures[:n]



