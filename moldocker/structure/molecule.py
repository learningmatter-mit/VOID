import random
import numpy as np
from pymatgen.core import Molecule
from pymatgen.analysis.local_env import JmolNN
from pymatgen.analysis.graphs import MoleculeGraph


class MoleculeAnalyzer:
    """Assorted tools to analyze a molecule and its parts"""
    def __init__(self, molecule):
        self.mol = molecule
        self.update_properties()

    def update_properties(self):
        self.rings = self.molgraph.find_rings()
        self.bonds = self.molgraph.graph.edges(data=False)

    @property
    def molgraph(self):
        return MoleculeGraph.with_local_env_strategy(self.mol, JmolNN())

    def get_twistable_bonds(self):
        return [
            [u, v]
            for u, v in self.bonds
            if self.is_twistable(u, v)
        ]

    def is_twistable(self, u, v):
        """Returns true if bond defined by indices u, v form
            a twistable bond"""
        return (
            not self.is_hydrogen(u)
            and not self.is_hydrogen(v)
            and not self.in_same_ring(u, v)
        )

    def is_hydrogen(self, idx):
        return self.mol[idx].species_string == 'H'

    def in_same_ring(self, u, v):
        return any([
            (u, v) in ring or (v, u) in ring
            for ring in self.rings
        ])


class MoleculeTransformer(MoleculeAnalyzer):
    def __init__(self, molecule):
        super().__init__(molecule)

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

    def substitute(self, fragment, atom=None):
        """Replaces the given atom by fragment"""
        if atom is None:
            hydrogens = [i for i in range(len(self.mol)) if self.is_hydrogen(i)]
            atom = random.sample(hydrogens, 1)[0]

        self.molgraph.substitute_group(atom, fragment, JmolNN)

        self.update_properties()
        
        return self.mol
