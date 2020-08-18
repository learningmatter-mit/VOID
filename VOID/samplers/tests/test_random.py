import numpy as np
import unittest as ut

from VOID.samplers import RandomSampler
from VOID.tests.test_inputs import load_structure, load_molecule


class TestRandomSampler(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.sampler = RandomSampler(num_samples=20)

    def test_points(self):
        points = self.sampler.get_points(self.host)
        self.assertEqual(len(points), 20)


if __name__ == "__main__":
    ut.main()
