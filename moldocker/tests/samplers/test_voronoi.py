import numpy as np
import unittest as ut

from moldocker.samplers import VoronoiSampler, VoronoiClustering
from ..test_inputs import load_structure, load_molecule


class TestVoronoi(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.sampler = VoronoiSampler()

    def test_points(self):
        points = self.sampler.get_points(self.host)
        expected = np.array([
            [ 2.94700000e+00,  7.81000000e-01,  5.25440000e-04],
            [ 0.00000000e+00,  0.00000000e+00,  5.25440000e-04],
            [ 2.15000000e+00,  2.16200000e+00,  4.30000000e+00],
            [ 7.97000000e-01,  2.94300000e+00,  5.25440000e-04],
            [ 0.00000000e+00,  0.00000000e+00,  2.15000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  4.30000000e+00],
            [-7.97000000e-01,  2.94300000e+00,  4.30000000e+00],
            [-3.98600000e+00,  1.12280000e+01,  4.30000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  6.45000000e+00],
            [ 1.09200000e+01,  7.81000000e-01,  4.30000000e+00],
            [ 3.98600000e+00,  1.12280000e+01,  5.25440000e-04],
            [ 1.17170000e+01,  2.16200000e+00,  5.25440000e-04],
            [ 4.78300000e+00,  9.84700000e+00,  4.30000000e+00],
            [ 6.13600000e+00,  9.06600000e+00,  8.60047456e+00],
            [ 7.73000000e+00,  9.06600000e+00,  4.30000000e+00],
            [-4.78300000e+00,  9.84700000e+00,  5.25440000e-04]
        ])
        self.assertIsNone(
            np.testing.assert_allclose(points, expected)
        )


class TestVoronoiClustering(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        self.guest = load_molecule()
        self.N = 4
        self.sampler = VoronoiClustering(n_clusters=self.N)

    def test_points(self):
        points = self.sampler.get_points(self.host)
        self.assertEqual(len(points), self.N)

if __name__ == "__main__":
    ut.main()
