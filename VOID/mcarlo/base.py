from VOID.object import ParseableObject


NUM_STEPS = 50


class MonteCarlo(ParseableObject):
    PARSER_NAME = "montecarlo"
    HELP = "Very basic Monte Carlo class. Nothing is implemented"

    def __init__(self, fitness, **kwargs):
        self.fitness = fitness

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

    def run(self, obj, num_steps):
        self.on_start(obj)

        for step in range(num_steps):
            self.on_trial_start(step)
            obj = self.trial(obj)
            self.on_trial_end(step)

        self.on_end(obj)
        return obj

    def trial(self, obj):
        return obj
