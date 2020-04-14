import numpy as np

from .mcmc import Action
from .metropolis import Metropolis


class Grower(Metropolis):
    PARSER_NAME = "grower"
    HELP = "Grows a guest inside a host."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Action
    def translate(self, cpx):
        return cpx.translate_guest()

    @Action
    def rotate(self, cpx):
        return cpx.rotate_guest()
