import os
from pymatgen.core import Structure, Molecule
import unittest as ut


thisdir = os.path.dirname(os.path.abspath(__file__))
inpath = os.path.join(thisdir, "files")


def load_structure(filename="AFI.cif"):
    path = os.path.join(inpath, filename)
    return Structure.from_file(path)


def load_molecule(filename="molecule.xyz"):
    path = os.path.join(inpath, filename)
    return Molecule.from_file(path)


class TestInputs(ut.TestCase):
    def setUp(self):
        self.structure = load_structure()
        self.molecule = load_molecule()

    def test_struct(self):
        self.assertEqual(len(self.structure), 72)

    def test_molecule(self):
        self.assertEqual(len(self.molecule), 47)


if __name__ == "__main__":
    ut.main()
