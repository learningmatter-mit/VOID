import numpy as np
from pymatgen.core import Molecule


class MoleculeTransformer:
    def __init__(self, molecule):
        self.mol = molecule

    def rotate(self, axis, theta, anchor):
        if anchor is None:
            anchor = self.mol.center_of_mass

        if axis is None:
            axis = np.random.randn(3)

        if theta is None:
            theta = 2 * np.pi * np.random.uniform()

        self.mol.rotate_sites(axis=axis, theta=theta, anchor=anchor)
        return self.mol

    def translate(self, vector):
        if vector is None:
            vector = np.random.randn(3)

        self.mol.translate_sites(vector=vector)
        return self.mol

