import numpy as np

from moldocker.mcarlo import Metropolis, Action


class MonteCarloDocker(Metropolis):
    PARSER_NAME = "mcdocker"
    HELP = "Repeats actions such as docking, translating and rotating the molecule until the metric is improved"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Action
    def translate(self, cpx):
        return cpx.translate_guest()

    @Action
    def rotate(self, cpx):
        return cpx.rotate_guest()

