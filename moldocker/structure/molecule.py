import random
import numpy as np
import networkx as nx
from pymatgen.core import Molecule
from pymatgen.analysis.local_env import JmolNN
from pymatgen.analysis.graphs import MoleculeGraph


HYDROGEN_CUTOFF = 1.2


class MoleculeAnalyzer:
    """Assorted tools to analyze a molecule and its parts"""
    def __init__(self, molecule):
        self.mol = molecule
        self.update_properties()

    def update_properties(self):
        self.molgraph = MoleculeGraph.with_local_env_strategy(self.mol, JmolNN())
        #self.rings = self.molgraph.find_rings()
        self.rings = self.find_rings()
        self.bonds = self.molgraph.graph.edges(data=False)

    def find_rings(self):
        G = nx.Graph(self.molgraph.graph)
        return list(nx.algorithms.cycles.cycle_basis(G))

    def get_twistable_bonds(self):
        bonds = [
            [u, v]
            for u, v in self.bonds
            if self.is_twistable(u, v)
        ]

        if len(bonds) == 0:
            return self.get_bonds_outside_rings()

        return bonds

    def get_bonds_outside_rings(self):
        return [
            [u, v]
            for u, v in self.bonds
            if not self.in_same_ring(u, v)
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
            u in ring and v in ring
            for ring in self.rings
        ])

    def get_hydrogens(self):
        return [i for i in range(len(self.mol)) if self.is_hydrogen(i)]

    def get_non_hydrogen_neighbors(self, atom):
        return [nbr
            for nbr in self.mol.get_neighbors(self.mol[atom], HYDROGEN_CUTOFF)
            if not self.is_hydrogen(nbr.index)
        ]

    def find_hydrogen_bridges(self):
        """Get hydrogens which are close to two heavier atoms"""
        hydrogens = self.get_hydrogens()

        num_nbrs = [
            len(self.get_non_hydrogen_neighbors(i))
            for i in hydrogens
        ]

        return [
            site
            for site, n in zip(hydrogens, num_nbrs)
            if n >= 2
        ]


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
            atom = random.sample(self.get_hydrogens(), 1)[0]

        self.molgraph.substitute_group(atom, fragment, JmolNN)

        self.update_properties()
        
        return self.mol

    def close_ring(self, atom=None):
        """Creates a ring between close atoms"""
        raise NotImplementedError

