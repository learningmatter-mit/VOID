import random
from moldocker.object import ParseableObject


NUM_STEPS = 50


class MonteCarlo(ParseableObject):
    PARSER_NAME = "montecarlo"
    HELP = "Very basic Monte Carlo class. Nothing is implemented"

    def __init__(self, metric, num_steps,  **kwargs):
        self.metric = metric
        self.num_steps = num_steps
        self.actions = self.make_actions()

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--num_steps",
            type=int,
            help="maximum number of Monte Carlo steps (default: %(default)s)",
            default=NUM_STEPS,
        )

    def on_start(self, obj):
        pass

    def on_end(self, obj):
        pass

    def on_trial_start(self, step):
        pass

    def on_trial_end(self, step):
        pass

    def run(self, obj):
        self.on_start(obj)

        for step in range(self.num_steps):
            self.on_trial_start(step)
            obj = self.run_trial(obj)
            self.on_trial_end(step)

        self.on_end(obj)
        return obj

    def run_trial(self, obj):
        return obj


class MarkovChainMC(MonteCarlo):
    PARSER_NAME = "mcmc"
    HELP = "Markov Chain Monte Carlo simulation. Updates an object based on given actions and acceptance criterion"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_actions(self):
        actions = {}
        def mkaction(func):
            actions[func.__name__] = func
            return func

        mkaction.all = actions
        return mkaction

    def run_trial(self, obj):
        action = self.sample_action()
        newobj = action(obj)

        if self.accept(newobj, obj):
            obj = newobj

        return obj

    def sample_action(self):
        return random.sample(self.actions.all, 1)

    def accept(self, new, old):
        return np.random.uniform() >= 0.5


class Metropolis(MarkovChainMC):
    PARSER_NAME = "metropolis"
    HELP = "Try different actions onto a given object to maximize the given metric using the Metropolis-Hastings algorithm"

    def __init__(self, *args, temperature, temperature_profile=None, **kwargs):
        """
        Args:
            temperature (float)
            temperature_profile (callable)
        """
        super().__init__(*args, **kwargs)
        self.temperature = temperature
        if temperature_profile is None:
            self.temperature_profile = lambda step: return temperature
        else:
            assert hasattr(temperature_profile, '__call__'), "Temperature profile is not callable"
            self.temperature_profile = temperature_profile

    def accept(self, new, old):
        delta_e = self.metric(new) - self.metric(old)
        return np.exp(-delta_e / self.temperature) > np.random.uniform()

    def on_trial_end(self, step):
        self.update_temperature(step)

    def update_temperature(self, step):
        self.temperature = self.temperature_profile(step)



