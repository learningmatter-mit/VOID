import copy
import random
import inspect
import numpy as np

from .base import MonteCarlo


class MarkovChainMC(MonteCarlo):
    PARSER_NAME = "mcmc"
    HELP = "Markov Chain Monte Carlo simulation. Updates an object based on given actions and acceptance criterion"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_actions(self):
        return Action.get_actions(self)

    def trial(self, obj):
        action = self.sample_action()

        newobj = action(self, copy.deepcopy(obj))

        if self.accept(newobj, obj):
            obj = newobj

        return obj

    def sample_action(self):
        actions = self.get_actions()
        return random.sample(actions, 1)[0]

    def accept(self, new, old):
        return np.random.uniform() >= 0.5


class Action:
    """Decorator that defines an action for MCMC-derived classes.
        It basically appends the function `action` itself as an attribute
        of the new method.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @staticmethod
    def is_action(obj):
        return isinstance(obj, Action)

    @staticmethod
    def get_actions(cls):
        """Return methods in `cls` that are actions"""
        return [
            fn
            for name, fn in inspect.getmembers(cls, Action.is_action)
        ]
