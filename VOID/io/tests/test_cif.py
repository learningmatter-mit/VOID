import os
import shutil
import unittest as ut

from VOID.io import cif
from VOID.tests.test_inputs import load_structure, load_molecule, inpath


class TestCif(ut.TestCase):
    def setUp(self):
        self.structure = load_structure()

    def test_load(self):
        path = os.path.join(inpath, "AFI.cif")
        loaded = cif.read_cif(path, primitive=False)
        self.assertEqual(self.structure, loaded)

    def test_write(self):
        scratchdir = ".tmp_test"
        if not os.path.exists(scratchdir):
            os.mkdir(scratchdir)

        outpath = os.path.join(scratchdir, "test.cif")

        cif.write_cif(outpath, self.structure)
        loaded = cif.read_cif(outpath, primitive=False)

        self.assertEqual(self.structure, loaded)

        shutil.rmtree(scratchdir)


if __name__ == "__main__":
    ut.main()
