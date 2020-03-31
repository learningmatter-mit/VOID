import numpy as np
from tqdm import tqdm
from sklearn.cluster import KMeans

from moldocker.dockers.base import Docker
from docking.zeolite import voronoi
import docking.zeolite.utils as zeoutils


CLEARANCE = 1.0
DEFAULT_ATTEMPTS = 100
VORONOI_POINTS = 10
BEST_STRUCTURES = 10
MAX_LOADING = True


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
            probe_radius=probe_radius, remove_oxygen=remove_oxygen
        )
        self.nodes = voronoi_nodes_creator(self.substrate, min_radius=min_radius)
        self.num_voronoi_points = num_voronoi_points

    def select_best_structures(self, structures, n=BEST_STRUCTURES):
        """Select the best structures from the given list
            based on the goodness of fit of the molecule
            inside the pore.

        Args:
            structures (list of Structure)
            n (int): number of structures to select
        """
        fitness = [
            zeoutils.get_molecule_structure_distances(struct, len(self.substrate))
            for struct in structures
        ]

        best_structures = [
            st
            for st, _ in sorted(
                zip(structures, fitness), key=lambda x: x[1], reverse=True
            )
        ]

        return best_structures[:n]
