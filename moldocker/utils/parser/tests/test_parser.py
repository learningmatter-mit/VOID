import numpy as np
import unittest as ut

from moldocker.utils.parser.base import Parser


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse(self):
        args = [
            "../../tests/files/AFI.cif",
            "../../tests/files/molecule.xyz",
            "--docker",
            "batch",
            "--sampler",
            "voronoi_cluster",
            "--fitness",
            "min_distance",
            "--mcarlo",
            "grower",
            "--subdock",
        ]

        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.docker, "batch")
        self.assertEqual(parsed.sampler, "voronoi_cluster")
        self.assertEqual(parsed.fitness, "min_distance")
        self.assertEqual(parsed.mcarlo, "grower")


if __name__ == "__main__":
    ut.main()
