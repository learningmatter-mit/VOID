import os
import unittest as ut
from pymatgen.core import Structure, Molecule
from pymatgen.io.xyz import XYZ


thisdir = os.path.dirname(os.path.abspath(__file__))
inpath = os.path.join(thisdir, "files")


def load_structure(filename="AFI.cif"):
    path = os.path.join(inpath, filename)
    return Structure.from_file(path)


def load_molecule(filename="molecule.xyz"):
    path = os.path.join(inpath, filename)
    return Molecule.from_file(path)


def load_fragments(filename="fragments.xyz"):
    path = os.path.join(inpath, filename)
    xyz = XYZ.from_file(path)
    return xyz.all_molecules


class TestInputs(ut.TestCase):
    def setUp(self):
        self.structure = load_structure()
        self.molecule = load_molecule()
        self.fragments = load_fragments()

    def test_struct(self):
        self.assertEqual(len(self.structure), 72)

    def test_molecule(self):
        self.assertEqual(len(self.molecule), 47)

    def test_fragments(self):
        self.assertEqual(len(self.fragments), 11)


if __name__ == "__main__":
    ut.main()
