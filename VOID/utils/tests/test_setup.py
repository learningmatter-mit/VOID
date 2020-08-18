import os
import unittest as ut
from argparse import Namespace

from VOID.utils.setup import SetupRun
from VOID import dockers, samplers, fitness
from VOID.tests.test_inputs import load_structure, load_molecule


thisdir = os.path.dirname(os.path.abspath(__file__))


class TestSetup(ut.TestCase):
    def setUp(self):
        host_file = os.path.join(thisdir, "../../tests/files/AFI.cif")
        guest_file = os.path.join(thisdir, "../../tests/files/molecule.xyz")

        args = Namespace(
            **dict(
                input=[host_file, guest_file],
                docker="batch",
                sampler="voronoi_cluster",
                fitness="min_distance",
                subdock=True,
                max_subdock=1,
            )
        )

        self.setup = SetupRun(args)

    def test_sampler(self):
        sampler = self.setup.get_sampler()
        self.assertIsInstance(sampler, samplers.VoronoiClustering)

    def test_fitness(self):
        fit = self.setup.get_fitness()
        self.assertIsInstance(fit, fitness.MinDistanceFitness)

    def test_structures(self):
        host, guest = self.setup.get_structures()
        host_ref = load_structure()
        guest_ref = load_molecule()
        self.assertEqual(host, host_ref)
        self.assertEqual(guest, guest_ref)

    def test_docker(self):
        docker = self.setup.get_docker()
        self.assertIsInstance(docker, dockers.BatchDocker)

    def test_subdocker(self):
        subdocker = self.setup.get_subdocker()
        self.assertIsInstance(subdocker, dockers.Subdocker)


class TestSetupMonteCarlo(ut.TestCase):
    def setUp(self):
        host_file = os.path.join(thisdir, "../../tests/files/AFI.cif")
        guest_file = os.path.join(thisdir, "../../tests/files/molecule.xyz")

        args = Namespace(
            **dict(
                input=[host_file, guest_file],
                docker="mcdocker",
                sampler="voronoi_cluster",
                fitness="min_distance",
                subdock=True,
                max_subdock=1,
                temperature=0.1
            )
        )

        self.setup = SetupRun(args)

    def test_docker(self):
        docker = self.setup.get_docker()
        self.assertIsInstance(docker, dockers.MonteCarloDocker)



if __name__ == "__main__":
    ut.main()
