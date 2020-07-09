import numpy as np

from .base import Docker
from moldocker.structure import Complex
from moldocker.utils.geometry import random_rotation_matrices


class SerialDocker(Docker):
    PARSER_NAME = "serial"
    HELP = "Docks guests to host using serial operations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rotate_guest(self):
        coords = self.guest.cart_coords
        rotation = random_rotation_matrices(1)

        return np.matmul(coords, rotation)

    def translate_host(self, point):
        return self.host.cart_coords - point

    def dock_at_point(self, point, attempts):
        hcoords = self.translate_host(point)

        complexes = [
            Complex(
                self.new_host(newcoords=hcoords),
                self.new_guest(newcoords=self.rotate_guest())
            )
            for _ in range(attempts)
        ]

        return complexes

