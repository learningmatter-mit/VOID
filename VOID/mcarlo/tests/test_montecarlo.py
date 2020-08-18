import numpy as np
import unittest as ut

from VOID.mcarlo import MonteCarlo
from VOID.fitness import Fitness

from VOID.tests.test_inputs import load_structure, load_molecule


class ExampleMC(MonteCarlo):
    def trial(self, obj):
        return obj + 1


class TestMonteCarlo(ut.TestCase):
    def setUp(self):
        self.fitness = Fitness(threshold=1.5)
        self.num_steps = 10
        self.mcarlo = ExampleMC(self.fitness)

    def test_examplemc(self):
        initial = 0
        final = self.mcarlo.run(initial, self.num_steps)

        self.assertEqual(final, initial + self.num_steps)


if __name__ == "__main__":
    ut.main()
