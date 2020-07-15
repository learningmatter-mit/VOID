"""
Gets Voronoi nodes for zeolites using Zeo++ and its interface with pymatgen.
Requires changes in the pymatgen interface to work correctly.
"""

import numpy as np
from sklearn.cluster import KMeans
import pymatgen.io.zeopp as zeopp
from pymatgen.core.periodic_table import Specie
from pymatgen.analysis.bond_valence import BVAnalyzer

from .base import Sampler
from moldocker.io.stdout import suppress_stdout


PROBE_RADIUS = 0.1
MIN_VORONOI_RADIUS = 3.0
REMOVE_SPECIES = []
NUM_CLUSTERS = 10
PYMATGEN_RADII = False


class VoronoiSampler(Sampler):
    PARSER_NAME = "voronoi"
    HELP = "Samples the structure based on the voronoi \
            diagram of the void space"

    def __init__(
        self,
        probe_radius=PROBE_RADIUS,
        remove_species=REMOVE_SPECIES,
        min_radius=MIN_VORONOI_RADIUS,
        pymatgen_radii=PYMATGEN_RADII,
        **kwargs
    ):
        self.probe_radius = probe_radius
        self.remove_species = remove_species
        self.min_radius = min_radius
        self.pymatgen_radii = pymatgen_radii

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--probe_radius",
            type=float,
            help="radius of the probe to be used in voronoi diagrams (default: %(default)s)",
            default=PROBE_RADIUS,
        )
        parser.add_argument(
            "--remove_species",
            type=str,
            nargs="+",
            help="species to remove from the structure when computing voronoi diagrams (default: %(default)s)",
            default=REMOVE_SPECIES,
        )
        parser.add_argument(
            "--min_radius",
            type=float,
            help="minimum radius of a voronoi point for it to be considered during sampling (default: %(default)s)",
            default=MIN_VORONOI_RADIUS,
        )

    def remove_species_from_structure(self):
        for species in self.remove_species:
            self._structure.remove_species(species)

    def get_voronoi_structures(self):
        radii = self.get_atomic_radii()

        with suppress_stdout():
            nodes, edge_center, face_center = zeopp.get_voronoi_nodes(
                self._structure, radii, probe_rad=self.probe_radius
            )

        return nodes, edge_center, face_center

    def get_atomic_radii(self):
        if not self.pymatgen_radii:
            return None

        try:
            bv = BVAnalyzer()
            valences = bv.get_valences(self._structure)
            elements = [site.species_string for site in self._structure.sites]

            valence_dict = dict(zip(elements, valences))
            radii = {}
            for k, v in valence_dict.items():
                radii[k] = float(Specie(k, v).ionic_radius)

        except (ValueError, TypeError) as e:
            radii = None

        return radii

    def remove_close_nodes(self, nodes):
        """Removes voronoi nodes with radius smaller than
            `radius`.
        """

        remove_idx = [
            idx
            for idx, site in enumerate(nodes.sites)
            if site.properties["voronoi_radius"] < self.min_radius
        ]
        nodes.remove_sites(remove_idx)

        return nodes

    def get_voronoi_nodes(self, structure):
        self._structure = structure.copy()
        self.remove_species_from_structure()

        nodes, _, _ = self.get_voronoi_structures()
        nodes = self.remove_close_nodes(nodes)

        return nodes

    def get_points(self, structure):
        nodes = self.get_voronoi_nodes(structure)
        return nodes.cart_coords


class VoronoiClustering(VoronoiSampler):
    """Select best sites according to a k-means clustering
        algorithm. It provides us with a better selection of
        which points to try in the zeolite. Periodic boundary
        conditions are NOT taken into consideration when
        calculating the distances. The best sites are those
        further away from the zeolite (largest voronoi radius).
    """

    PARSER_NAME = "voronoi_cluster"
    HELP = "Samples the structure based on the voronoi \
            diagram of the void space plus clustering of \
            the voronoi nodes to lower the number of points \
            being searched"

    def __init__(self, *args, num_clusters=NUM_CLUSTERS, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_clusters = num_clusters

    @staticmethod
    def add_arguments(parser):
        super(VoronoiClustering, VoronoiClustering).add_arguments(parser)
        parser.add_argument(
            "--num_clusters",
            type=int,
            help="number of clusters to consider when sampling the structure with voronoi points (default: %(default)s)",
            default=NUM_CLUSTERS,
        )

    def get_points(self, structure):
        nodes = self.get_voronoi_nodes(structure)

        def cluster_points(X):
            num_clusters = min(len(X), self.num_clusters)
            kmeans = KMeans(n_clusters=num_clusters)
            kmeans.fit(X)
            return kmeans.labels_

        def select_sites(sites, labels):
            """Gets the best Voronoi sites for each clustering label.
                This is useful, as we want to minimize the number of
                attempts during docking.
            """
            best_sites = []
            for i in range(self.num_clusters):
                sites_cluster = [
                    site for site, cluster in zip(sites, labels) if cluster == i
                ]

                if len(sites_cluster) > 0:
                    best_site = max(
                        sites_cluster,
                        key=lambda site: site.properties["voronoi_radius"],
                    )

                    best_sites.append(best_site)

            return best_sites

        if len(nodes.cart_coords) == 0:
            return []

        clusters = cluster_points(nodes.cart_coords)
        best_sites = select_sites(nodes.sites, clusters)

        if len(best_sites) == 0:
            return []

        return [site.coords for site in best_sites]
