import numpy as np
from .mcmc import MarkovChainMC


TEMPERATURE = 0.1
ATTEMPTS = 200


class Metropolis(MarkovChainMC):
    PARSER_NAME = "metropolis"
    HELP = "Try different actions onto a given object to maximize the given fitness using the Metropolis-Hastings algorithm"

    def __init__(self, *args, temperature, temperature_profile=None, **kwargs):
        """
        Args:
            temperature (float)
            temperature_profile (callable)
        """
        super().__init__(*args, **kwargs)
        self.temperature = temperature
        self.temperature_profile = self.set_temperature_profile(temperature_profile)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--attempts",
            type=int,
            help="maximum number of Monte Carlo steps (default: %(default)s)",
            default=ATTEMPTS,
        )

        parser.add_argument(
            "--temperature",
            type=float,
            help="temperature of the calculation (default: %(default)s)",
            default=TEMPERATURE,
        )

    def set_temperature_profile(self, profile):
        if profile is None:
            return lambda step: self.temperature

        assert hasattr(profile, "__call__"), "Temperature profile is not callable"
        return profile

    def accept(self, new, old):
        """Convention: Metropolis tries to maximize the fitness"""
        # accept if the new fitness is larger than the old one
        delta_e = self.fitness(old) - self.fitness(new)

        if self.temperature == 0:
            return delta_e < 0

        return np.exp(-delta_e / self.temperature) > np.random.uniform()

    def on_trial_end(self, step):
        self.update_temperature(step)

    def update_temperature(self, step):
        self.temperature = self.temperature_profile(step)
        return self.temperature
