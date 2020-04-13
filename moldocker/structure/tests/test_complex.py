import numpy as np
import unittest as ut

from moldocker.structure import Complex
from moldocker.utils.geometry import rotation_matrix
from moldocker.tests.test_inputs import load_structure, load_molecule


class TestComplex(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.complex = Complex(self.host.copy(), self.guest.copy())

    def test_rotate(self):
        axis = np.array([0, 0, 1])
        theta = np.pi / 4
        newguest = self.complex.rotate_guest(axis, theta)
        oldguest = self.guest.get_centered_molecule()

        rot = rotation_matrix(axis, theta)
        newcoords = oldguest.cart_coords @ rot.T + self.guest.center_of_mass

        self.assertTrue(np.allclose(newguest.cart_coords, newcoords))

    def test_translate(self):
        vec = np.array([0, 0, 1])
        newguest = self.complex.translate_guest(vec)

        newcoords = self.guest.cart_coords + vec

        self.assertTrue(np.allclose(newguest.cart_coords, newcoords))


if __name__ == "__main__":
    ut.main()
