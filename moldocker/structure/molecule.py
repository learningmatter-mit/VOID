import random
import numpy as np
from pymatgen.core import Molecule
from pymatgen.analysis.local_env import JmolNN
from pymatgen.analysis.graphs import MoleculeGraph


class MoleculeTransformer:
    def __init__(self, molecule):
        self.mol = molecule

    @property
    def molgraph(self):
        return MoleculeGraph.with_local_env_strategy(self.mol, JmolNN())

    def rotate(self, axis=None, theta=None, anchor=None, indices=None):
        if anchor is None:
            anchor = self.mol.center_of_mass

        if axis is None:
            axis = np.random.randn(3)

        if theta is None:
            theta = 2 * np.pi * np.random.uniform()

        self.mol.rotate_sites(indices=indices, axis=axis, theta=theta, anchor=anchor)
        return self.mol

    def translate(self, vector=None):
        if vector is None:
            vector = np.random.randn(3)

        self.mol.translate_sites(vector=vector)
        return self.mol

    def twist_bond(self, bond=None, theta=None):
        if bond is None:
            bond = random.sample(self.get_twistable_bonds(), 1)[0]

        axis = self.mol[bond[0]].coords - self.mol[bond[1]].coords
        anchor = self.mol[bond[0]].coords

        subgraphs = self.molgraph.split_molecule_subgraphs([bond], allow_reverse=True)
        fragment = random.sample(subgraphs, 1)[0]
        indices = [self.mol.index(site) for site in fragment.molecule]

        return self.rotate(axis=axis, theta=theta, anchor=anchor, indices=indices)

    def get_twistable_bonds(self):
        bonds = self.molgraph.graph.edges(data=True)
        bonds = [
            [u, v, data]
            for u, v, data in bonds
            if not self.is_hydrogen(u)
            and not self.is_hydrogen(v)
        ]

        twistable = []
        for u, v, _ in bonds:
            if not self.in_same_ring(u, v):
                twistable.append([u, v])

        return twistable

    def is_hydrogen(self, idx):
        return self.mol[idx].species_string == 'H'

    def in_same_ring(self, u, v):
        rings = self.molgraph.find_rings()
        return any([
            (u, v) in ring or (v, u) in ring
            for ring in rings
        ])




