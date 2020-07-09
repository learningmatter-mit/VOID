import numpy as np

from moldocker.dockers.serial import SerialDocker
from moldocker.structure import Complex
from moldocker.utils.geometry import random_rotation_matrices


class SuccessDocker(SerialDocker):
    PARSER_NAME = "success"
    HELP = "Docks guests to host until a successful docking is found"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dock_at_point(self, point, attempts):
        hcoords = self.translate_host(point)

        for trial in range(attempts):
            cpx = Complex(
                self.new_host(newcoords=hcoords),
                self.new_guest(newcoords=self.rotate_guest())
            )

            if self.fitness(cpx) >= 0:
                print(f"{trial + 1} attempts to success")
                return [cpx]

        return []
