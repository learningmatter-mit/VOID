import numpy as np
import unittest as ut

from VOID.utils.parser.base import Parser


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse(self):
        args = [
            "../../tests/files/AFI.cif",
            "../../tests/files/molecule.xyz",
        ]

        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.input[0], "../../tests/files/AFI.cif")
        self.assertEqual(parsed.input[1], "../../tests/files/molecule.xyz")


if __name__ == "__main__":
    ut.main()
