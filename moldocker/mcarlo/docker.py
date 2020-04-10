from .base import MonteCarlo


class MonteCarloDocker(MonteCarlo):
    PARSER_NAME = "mcdocker"
    HELP = "Repeats actions such as docking, translating and rotating the molecule until the metric is maximized"

    def __init__(self, num_steps, docker, **kwargs):
        super().__init__(num_steps, **kwargs)

