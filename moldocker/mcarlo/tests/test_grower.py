import numpy as np
import unittest as ut

from moldocker.mcarlo import Grower
from moldocker.structure import FragmentCreator, Complex
from moldocker.fitness import MinDistanceFitness
from moldocker.tests.test_inputs import load_fragments, load_structure


class TestGrower(ut.TestCase):
    def setUp(self):
        self.host = load_structure()
        fragments = load_fragments()
        self.fragments = [
            FragmentCreator(frag.copy()).get_fragment()
            for frag in fragments
        ]
        self.seed = fragments[0]
        self.complex = Complex(self.host, self.seed)
        self.fitness = MinDistanceFitness(threshold=1.5)

        self.num_steps = 100
        self.temperature = 0

        self.mcdocker = Grower(
            fitness=self.fitness,
            temperature=self.temperature,
            fragments=self.fragments
        )

    def test_examplemc(self):
        cpx = self.mcdocker.run(self.complex.copy(), self.num_steps)
        import pdb
        pdb.set_trace()
        self.assertTrue(cpx.distance_matrix.min() > 1.5)


if __name__ == "__main__":
    ut.main()
