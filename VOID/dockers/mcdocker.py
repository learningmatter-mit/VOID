import numpy as np

from VOID.structure import Complex
from VOID.mcarlo import Metropolis, Action
from VOID.dockers import Docker


class MonteCarloDocker(Metropolis, Docker):
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

        return self.rank_complexes([cpx])

    def copy(self):
        return self.__class__(**self.__dict__.copy())

    def on_start(self, cpx):
        v = np.random.rand(1, 3)
        lattice = cpx.host.lattice.matrix
        translation = (v @ lattice).reshape(-1)

        cpx.guest_transform.translate(translation)
        return cpx
