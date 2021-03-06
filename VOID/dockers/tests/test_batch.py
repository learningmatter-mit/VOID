import numpy as np
import unittest as ut

from VOID.dockers import BatchDocker
from VOID.samplers import OriginSampler
from VOID.fitness import MinDistanceFitness

from VOID.tests.test_inputs import load_structure, load_molecule


class TestBatch(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.sampler = OriginSampler()
        self.fitness = MinDistanceFitness(threshold=1.5)
        self.docker = BatchDocker(
            self.host, self.guest, self.sampler, fitness=self.fitness
        )

    def test_rotate(self):
        coords = self.docker.rotate_guest(10)

        self.assertEqual(coords.shape, (10, 47, 3))

    def test_translate(self):
        point = np.array([0, 0, 1])
        coords = self.docker.translate_host(point, 10)
        self.assertEqual(coords.shape, (10, 72, 3))

    def test_dock(self):
        complexes = []
        while len(complexes) == 0:
            complexes = self.docker.dock(10)

        self.assertIsInstance(complexes, list)

        pose = complexes[0].pose
        self.assertEqual(len(pose), 119)

        self.assertTrue(pose.distance_matrix[:72, 72:].min() > 1.5)


if __name__ == "__main__":
    ut.main()
