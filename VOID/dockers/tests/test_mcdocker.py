import numpy as np
import unittest as ut

from VOID.structure import Complex
from VOID.dockers import MonteCarloDocker
from VOID.samplers import OriginSampler
from VOID.fitness import MinDistanceFitness

from VOID.tests.test_inputs import load_structure, load_molecule


class TestMCDocker(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.complex = Complex(self.host, self.guest)
        self.fitness = MinDistanceFitness(threshold=1.5)

        self.num_steps = 100
        self.temperature = 0.1

        self.mcdocker = MonteCarloDocker(
            self.host, self.guest,
            fitness=self.fitness, temperature=self.temperature
        )

    def test_run(self):
        cpx = self.mcdocker.run(self.complex.copy(), self.num_steps)
        self.assertTrue(cpx.distance_matrix.min() > 1.5)

    def test_dock(self):
        cpxs = self.mcdocker.dock(self.num_steps)
        self.assertIsInstance(cpxs, list)
        self.assertIsInstance(cpxs[0], Complex)

    def test_copy(self):
        newdocker = self.mcdocker.copy()

        self.assertEqual(newdocker.temperature, self.mcdocker.temperature)
        self.assertEqual(newdocker.host, self.mcdocker.host)
        self.assertEqual(newdocker.guest, self.mcdocker.guest)


if __name__ == "__main__":
    ut.main()
