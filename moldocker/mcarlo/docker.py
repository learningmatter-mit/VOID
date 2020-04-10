from .base import MonteCarlo


class MonteCarloDocker(Metropolis):
    PARSER_NAME = "mcdocker"
    HELP = "Repeats actions such as docking, translating and rotating the molecule until the metric is maximized"

    def __init__(self, *args, docker, **kwargs):
        super().__init__(*args, **kwargs)

    @self.action
    def translate(self, cpx):
        raise NotImplementedError

    @self.action
    def rotate(self, cpx):
        raise NotImplementedError

    @self.action
    def dock(self, cpx):
        raise NotImplementedError

