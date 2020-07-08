import random
import numpy as np

from .mcmc import Action
from .metropolis import Metropolis


class Grower(Metropolis):
    PARSER_NAME = "grower"
    HELP = "Grows a guest inside a host."

    def __init__(self, *args, fragments, **kwargs):
        super().__init__(*args, **kwargs)
        self.fragments = fragments

    def sample_fragment(self):
        return random.sample(self.fragments, 1)[0]

    @Action
    def translate(self, cpx):
        cpx.guest_transform.translate()
        return cpx

    @Action
    def rotate(self, cpx):
        cpx.guest_transform.rotate()
        return cpx

    @Action
    def twist_bond(self, cpx):
        cpx.guest_transform.twist_bond()
        return cpx

    @Action
    def grow(self, cpx):
        frag = self.sample_fragment()

        try:
            cpx.guest_transform.substitute(frag)
        except RuntimeError:
            pass

        return cpx

