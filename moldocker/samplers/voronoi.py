"""
Gets Voronoi nodes for zeolites using Zeo++ and its interface with pymatgen.
Requires changes in the pymatgen interface to work correctly.
"""

import numpy as np
from pymatgen.core.periodic_table import Specie
import pymatgen.io.zeopp as zeopp
from pymatgen.analysis.bond_valence import BVAnalyzer

from moldocker import utils

from .base import Sampler


PROBE_RADIUS = 0.1
REMOVE_OXYGEN = True
MIN_VORONOI_RADIUS = 3.0


class VoronoiSampler(Sampler):
    def __init__(
        self,
        probe_radius=PROBE_RADIUS,
        remove_oxygen=REMOVE_OXYGEN,
        min_radius=MIN_VORONOI_RADIUS,
        **kwargs
    ):
        self.probe_radius = probe_radius
        self.remove_oxygen = remove_oxygen
        self.min_radius = min_radius

    def remove_oxygen_from_structure(self):
        self._structure.remove_species("O")

    def get_voronoi_nodes(self):
        try:
            radii = self.get_atomic_radii()
        except (ValueError, TypeError) as e:
            radii = None

        nodes, edge_center, face_center = zeopp.get_voronoi_nodes(
            self._structure, radii, probe_rad=self.probe_radius
        )

        return nodes, edge_center, face_center

    def get_atomic_radii(self):
        bv = BVAnalyzer()
        valences = bv.get_valences(self._structure)
        elements = [site.species_string for site in self._structure.sites]

        valence_dict = dict(zip(elements, valences))
        radii = {}
        for k, v in valence_dict.items():
            radii[k] = float(Specie(k, v).ionic_radius)

        return radii

    def remove_close_nodes(self, nodes, radius):
        """Removes voronoi nodes with radius smaller than
            `radius`.
        """

        remove_idx = [
            idx
            for idx, site in enumerate(nodes.sites)
            if site.properties["voronoi_radius"] < radius
        ]
        nodes.remove_sites(remove_idx)

        return nodes

    def get_points(self, structure):
        self._structure = structure.copy()
        if self.remove_oxygen:
            self.remove_oxygen_from_structure()

        nodes, _, _ = self.get_voronoi_nodes()
        nodes = self.remove_close_nodes(nodes, min_radius)

        return nodes


class VoronoiClustering(VoronoiSampler):
    def __init__(self, *args, n_clusters, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_clusters = n_clusters

    def get_docking_points(self):
        """Select best sites according to a k-means clustering
            algorithm. It provides us with a better selection of
            which points to try in the zeolite. Periodic boundary
            conditions are NOT taken into consideration when
            calculating the distances. The best sites are those
            further away from the zeolite (largest voronoi radius).
        """

        def cluster_points(X):
            n_clusters = min(len(X), self.n_clusters)
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(X)
            return kmeans.labels_

        def select_sites(sites, labels):
            best_sites = []
            for i in range(self.n_clusters):
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

        if len(self.nodes.cart_coords) == 0:
            return []

        clusters = cluster_points(self.nodes.cart_coords)
        best_sites = select_sites(self.nodes.sites, clusters)

        if len(best_sites) == 0:
            return []
        return [site.coords for site in best_sites]
