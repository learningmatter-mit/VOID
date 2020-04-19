import numpy as np
import unittest as ut

from moldocker.structure import FragmentCreator
from moldocker.tests.test_inputs import load_fragments


class TestFragment(ut.TestCase):
    def setUp(self):
        self.fragments = load_fragments()
        self.creator = FragmentCreator(self.fragments[2].copy())

    def test_radical(self):
        frag = self.creator.get_fragment()
        self.assertTrue(frag[0].species_string == "X0+")

    def test_small_frag(self):
        frag = self.fragments[10]
        newfrag = FragmentCreator(frag.copy()).get_fragment()

    def test_all_fragments(self):
        for idx, frag in enumerate(self.fragments):
            newfrag = FragmentCreator(frag.copy()).get_fragment()


if __name__ == "__main__":
    ut.main()
