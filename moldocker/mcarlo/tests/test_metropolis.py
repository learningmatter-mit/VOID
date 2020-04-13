import numpy as np
import unittest as ut

from moldocker.mcarlo import Metropolis, Action


def example_metric(number):
    return number


class ExampleMetropolis(Metropolis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Action
    def increment(self, obj):
        return obj + 1

    @Action
    def decrement(self, obj):
        return obj - 1


class TestMetropolis(ut.TestCase):
    def setUp(self):
        self.fitness = example_metric
        self.num_steps = 10
        self.num_loops = 20
        self.temperature = 1
        self.mcarlo = ExampleMetropolis(
            self.fitness,
            temperature=self.temperature
        )

    def test_actions(self):
        self.assertEqual(len(self.mcarlo.get_actions()), 2)

    def test_examplemc(self):
        initial = 0
        final = self.mcarlo.run(initial, self.num_steps)
        self.assertTrue(final <= self.num_steps)
        self.assertTrue(final >= -self.num_steps)

    def test_loopmc(self):
        initial = 0
        values = [
            self.mcarlo.run(initial, self.num_steps)
            for _ in range(self.num_loops)
        ]

        self.assertTrue(np.mean(values) < 0)

    def test_temperature(self):
        def profile(step):
            if step < 5:
                return 1
            return 0

        self.mcarlo.temperature_profile = self.mcarlo.set_temperature_profile(profile)

        self.assertEqual(self.mcarlo.update_temperature(0), 1)
        self.assertAlmostEqual(self.mcarlo.update_temperature(5), 0, places=5)
        self.assertAlmostEqual(self.mcarlo.update_temperature(10), 0, places=5)


if __name__ == "__main__":
    ut.main()
