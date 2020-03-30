"""
Gets Voronoi nodes for zeolites using Zeo++ and its interface with pymatgen.
Requires changes in the pymatgen interface to work correctly.
"""

import numpy as np

from pymatgen.core.periodic_table import Specie
import pymatgen.io.zeopp as zeopp 
from pymatgen.analysis.bond_valence import BVAnalyzer

import docking.zeolite.utils as zeoutils


PROBE_RADIUS = 0.1
REMOVE_OXYGEN = True
MIN_VORONOI_RADIUS = 3.0


class VoronoiNodes:
    def __init__(
        self,
        probe_radius=PROBE_RADIUS,
        remove_oxygen=REMOVE_OXYGEN,
        **kwargs
    ):
        self.probe_radius = probe_radius
        self.remove_oxygen = remove_oxygen

    def remove_oxygen_from_structure(self):
        self._structure.remove_species('O')

    def get_voronoi_nodes(self):

        try:
            radii = self.get_atomic_radii()
        except (ValueError, TypeError) as e:
            radii = None

        nodes, edge_center, face_center = zeopp.get_voronoi_nodes(
            self._structure,
            radii,
            probe_rad=self.probe_radius
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
    
    def __call__(
        self,
        structure, 
        join_structures=False,
        min_radius=MIN_VORONOI_RADIUS
    ):
        self._structure = structure.copy()
        if self.remove_oxygen:
            self.remove_oxygen_from_structure()

        nodes, _, _ = self.get_voronoi_nodes()
        nodes = self.remove_clashing_nodes(nodes, min_radius)

        if join_structures:
            return zeoutils.join_structures(nodes, structure.copy())

        return nodes

    def remove_clashing_nodes(self, nodes, radius):
        """Removes voronoi nodes with radius smaller than
            `radius`.
        """

        remove_idx = [
            idx 
            for idx, site in enumerate(nodes.sites)
            if site.properties['voronoi_radius'] < radius
        ]
        nodes.remove_sites(remove_idx)

        return nodes

