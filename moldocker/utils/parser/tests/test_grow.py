import numpy as np
import unittest as ut

from moldocker.utils.parser import GrowParser


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = GrowParser()

    def test_parse(self):
        args = [
            "../../tests/files/AFI.cif",
            "../../tests/files/molecule.xyz",
            "--mcarlo",
            "grower",
        ]

        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.mcarlo, "grower")


if __name__ == "__main__":
    ut.main()
