import numpy as np
import unittest as ut

from moldocker.dockers import BatchDocker

from ..test_inputs import load_structure, load_molecule
from ..samplers.test_sampler import DummySampler


class TestBatch(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.sampler = DummySampler
        self.docker = BatchDocker(
            self.host,
            self.guest,
            self.sampler
        )

    def test_rotate(self):
        coords = self.docker.rotate_guest(10)

        self.assertEqual(coords.shape, (10, 47, 3))

    def test_translate(self):
        point = np.array([0, 0, 1])
        coords = self.docker.translate_host(point, 10)
        self.assertEqual(coords.shape, (10, 72, 3))

    def test_dock(self):
        poses = []
        while len(poses) == 0:
            poses = self.docker.dock(10)

        self.assertIsInstance(poses, list)

        pose = poses[0]
        self.assertEqual(len(pose), 119)

        self.assertTrue(pose.distance_matrix[:72, 72:].min() > 1.5)


if __name__ == '__main__':
    ut.main()
