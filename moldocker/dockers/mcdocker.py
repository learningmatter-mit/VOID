import numpy as np

from moldocker.structure import Complex
from moldocker.mcarlo import Metropolis, Action


class MonteCarloDocker(Metropolis):
    PARSER_NAME = "mcdocker"
    HELP = "Repeats actions such as docking, translating and rotating the molecule until the metric is improved"

    def __init__(self, host, guest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.guest = guest

    @Action
    def translate(self, cpx):
        cpx.guest_transform.translate()
        return cpx

    @Action
    def rotate(self, cpx):
        cpx.guest_transform.rotate()
        return cpx

    def dock(self, attempts):
        cpx = Complex(self.host.copy(), self.guest.copy())
        cpx = self.run(cpx, attempts)

        return [cpx]

    def copy(self):
        return self.__class__(
            self.host.copy(),
            self.guest.copy(),
            self.fitness,
            self.temperature,
            self.temperature_profile
        )
