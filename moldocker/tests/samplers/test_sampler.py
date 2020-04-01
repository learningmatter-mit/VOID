import numpy as np
import unittest as ut

from moldocker.samplers import OriginSampler
from ..test_inputs import load_structure, load_molecule


class TestSampler(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.sampler = OriginSampler()

    def test_points(self):
        points = self.sampler.get_points(self.host)
        self.assertIsInstance(points, list)
        np.testing.assert_allclose(points[0], 0)


if __name__ == "__main__":
    ut.main()
