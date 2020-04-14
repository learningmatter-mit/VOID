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
        self.assertTrue(frag[0].species_string == 'X0+')

if __name__ == "__main__":
    ut.main()
