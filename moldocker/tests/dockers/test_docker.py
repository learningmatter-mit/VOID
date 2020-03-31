import numpy as np
import unittest as ut

from moldocker.dockers import Docker
from moldocker.samplers import OriginSampler

from ..test_inputs import load_structure, load_molecule


class TestDocker(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.sampler = OriginSampler()
        self.docker = Docker(
            self.host,
            self.guest,
            self.sampler
        )

    def test_rotate(self):
        axis = np.array([0, 0, 1])
        theta = np.pi / 4
        M = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
        
        rot_coords = self.guest.cart_coords @ M.T

        new_guest = self.docker.rotate_guest(theta, axis)

        self.assertIsNone(np.testing.assert_allclose(rot_coords, new_guest.cart_coords))

    def test_translate(self):
        point = np.array([0, 0, 1])
        
        translated = self.host.lattice.get_fractional_coords(
            self.host.cart_coords - point
        ) % 1
        transl_host = self.docker.translate_host(point)

        np.testing.assert_allclose(translated, transl_host.frac_coords)

    def test_dock(self):
        poses = self.docker.dock(10)
        self.assertIsInstance(poses, list)


if __name__ == '__main__':
    ut.main()
