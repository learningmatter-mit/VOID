import numpy as np
import unittest as ut

from moldocker.mcarlo import Grower
from moldocker.structure import FragmentCreator, Complex
from moldocker.fitness import MinDistanceGaussianTarget, MinDistanceFitness, MultipleFitness
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

        self.target = 1.5
        self.tolerance = 0.2
        fitness = [
            MinDistanceGaussianTarget(target=self.target, tolerance=self.tolerance),
            MinDistanceFitness(threshold=0.85, structure='guest', step=True),
            MinDistanceFitness(threshold=1.1, structure='complex', step=True)
        ]
        weights = [5, 100, 100]
        self.fitness = MultipleFitness(fitness, weights)

        self.num_steps = 200
        self.temperature = 0.1

        self.mcdocker = Grower(
            fitness=self.fitness,
            temperature=self.temperature,
            fragments=self.fragments
        )

    def test_examplemc(self):
        cpx = self.mcdocker.run(self.complex.copy(), self.num_steps)
        self.assertTrue(np.abs(cpx.distance_matrix.min() - self.target) < self.tolerance)

        with open('/tmp/pose.cif', 'w') as f:
            f.write(cpx.pose.to('cif'))


if __name__ == "__main__":
    ut.main()
