import numpy as np
import unittest as ut

from VOID.structure import MoleculeTransformer
from VOID.utils.geometry import rotation_matrix
from VOID.tests.test_inputs import load_molecule


class TestTransformer(ut.TestCase):
    def setUp(self):
        self.guest = load_molecule()
        self.transformer = MoleculeTransformer(self.guest.copy())
        self.smallguest = load_molecule("ammonium.xyz")

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

        twbonds = self.transformer.get_twistable_bonds()
        self.assertEqual(len(twbonds), 1)

    @ut.skip("twisting bonds is not working so well for now")
    def test_twist(self):
        theta = np.pi / 4

        methyl = [0, 18, 19, 20]
        remaining = [i for i in range(len(self.guest)) if i not in methyl]

        newguest = self.transformer.twist_bond(theta=theta)

        oldguest = self.guest.copy()
        axis = oldguest[0].coords - oldguest[1].coords
        anchor = oldguest[0].coords

        if np.allclose(newguest.cart_coords[methyl], oldguest.cart_coords[methyl]):
            oldcoords = oldguest.cart_coords[remaining] - anchor
            newcoords = newguest.cart_coords[remaining] - anchor
        elif np.allclose(
            newguest.cart_coords[remaining], oldguest.cart_coords[remaining]
        ):
            oldcoords = oldguest.cart_coords[methyl] - anchor
            newcoords = newguest.cart_coords[methyl] - anchor
        else:
            raise AssertionError("both fragments of the molecule were changed!")

        rot = rotation_matrix(axis, theta)
        rotcoords = oldcoords @ rot.T
        self.assertTrue(np.allclose(newcoords, rotcoords))

    def test_twist_small_molecule(self):
        transformer = MoleculeTransformer(self.smallguest)
        try:
            newguest = self.transformer.twist_bond()
        except ValueError:
            self.fail("error while twisting the bond of a small molecule")


if __name__ == "__main__":
    ut.main()
