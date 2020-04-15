import numpy as np

from moldocker.mcarlo import Metropolis, Action


class MonteCarloDocker(Metropolis):
    PARSER_NAME = "mcdocker"
    HELP = "Repeats actions such as docking, translating and rotating the molecule until the metric is improved"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Action
    def translate(self, cpx):
        cpx.guest_transform.translate()
        return cpx

    @Action
    def rotate(self, cpx):
        cpx.guest_transform.rotate()
        return cpx

