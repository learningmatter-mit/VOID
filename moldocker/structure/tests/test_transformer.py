import numpy as np
import unittest as ut

from moldocker.structure import MoleculeTransformer
from moldocker.utils.geometry import rotation_matrix
from moldocker.tests.test_inputs import load_molecule


class TestTransformer(ut.TestCase):
    def setUp(self):
        self.guest = load_molecule()
        self.transformer = MoleculeTransformer(self.guest.copy())

    def test_rotate(self):
        axis = np.array([0, 0, 1])
        theta = np.pi / 4
        newguest = self.transformer.rotate(axis, theta)
        oldguest = self.guest.get_centered_molecule()

        rot = rotation_matrix(axis, theta)
        newcoords = oldguest.cart_coords @ rot.T + self.guest.center_of_mass

        self.assertTrue(np.allclose(newguest.cart_coords, newcoords))

    def test_translate(self):
        vec = np.array([0, 0, 1])
        newguest = self.transformer.translate(vec)

        newcoords = self.guest.cart_coords + vec

        self.assertTrue(np.allclose(newguest.cart_coords, newcoords))

    def test_bonds(self):
        molgraph = self.transformer.molgraph
        self.assertEqual(len(molgraph.graph.edges), 50)

        twbonds = self.transformer.twistable_bonds()
        self.assertEqual(len(twbonds), 1)



if __name__ == "__main__":
    ut.main()
