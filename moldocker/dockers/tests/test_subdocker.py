import numpy as np
import unittest as ut

from moldocker.structure import Complex
from moldocker.dockers import BatchDocker, Subdocker
from moldocker.samplers import OriginSampler
from moldocker.fitness import MinDistanceFitness

from moldocker.tests.test_inputs import load_structure, load_molecule


class TestSubdocker(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.sampler = OriginSampler()
        self.fitness = MinDistanceFitness(threshold=1.5)
        self.docker = BatchDocker(
            self.host, self.guest, self.sampler, fitness=self.fitness
        )
        self.subdocker = Subdocker(self.docker, 2)

    def test_dock(self):
        complexes = {}
        while len(complexes) == 0:
            complexes = self.subdocker.dock(10)

        self.assertIsInstance(complexes, list)
        self.assertIsInstance(complexes[0], Complex)

        pose = complexes[0].pose
        self.assertEqual(len(pose), 119)

        self.assertTrue(pose.distance_matrix[:72, 72:].min() > 1.5)


if __name__ == "__main__":
    ut.main()
