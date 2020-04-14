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
        self.molgraph = MoleculeGraph.with_local_env_strategy(self.mol, JmolNN())
        self.rings = self.molgraph.find_rings()
        self.bonds = self.molgraph.graph.edges(data=False)

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


class FragmentHandler:
    RADICAL_SPECIES = 'X0+'
    NBR_RADIUS = 1.5

    def __init__(self, frag):
        self.frag = frag

    def is_neighbor(self, atom, nbr):
        return nbr in self.frag.get_neighbors(atom, self.NBR_RADIUS)

    def is_species(self, atom, species):
        return atom.species_string == species

    def sample_terminal_atom(self):
        hydrogens = [at for at in self.frag if self.is_species(at, 'H')]
        return random.sample(hydrogens, 1)[0]

    def create_radical(self, atom=None):
        if atom is None:
            atom = self.sample_terminal_atom()

        nearest_nbr = [
            nbr
            for nbr in self.frag.get_neighbors(atom, self.NBR_RADIUS)
            if not self.is_species(nbr, 'H')
        ][0]

        self.frag.remove(atom)
        self.frag.remove(nearest_nbr)

        # insert the atoms again to reorder them
        self.frag.insert(0, self.RADICAL_SPECIES, atom.coords)
        self.frag.insert(1, nearest_nbr.species, nearest_nbr.coords)

        if not self.is_fragment_formatted():
            raise RuntimeError("Unknown error during formatting of fragment")

        return self.frag

    def is_fragment_formatted(self):
        return self.is_species(self.frag[0], self.RADICAL_SPECIES) and self.is_neighbor(self.frag[0], self.frag[1])

    def get_fragment(self):
        if self.is_fragment_formatted():
            return self.frag

        return self.create_radical()

