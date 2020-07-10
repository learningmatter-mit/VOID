import numpy as np

from .base import Docker
from moldocker.structure import Complex
from moldocker.utils.geometry import random_rotation_matrices


class BatchDocker(Docker):
    PARSER_NAME = "batch"
    HELP = "Docks guests to host by using batched (tensorial) operations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rotate_guest(self, attempts):
        # (N, num_atoms, 3) matrix
        coords = np.repeat(self.guest.cart_coords[None, ...], attempts, axis=0)

        # (N, 3, 3) matrix
        rotation = random_rotation_matrices(attempts)

        # (N, num_atoms, 3) matrix
        return np.matmul(coords, rotation.swapaxes(-1, -2))

    def translate_host(self, point, attempts):
        translated = self.host.cart_coords - point

        return np.repeat(translated[None, ...], attempts, axis=0)

    def dock_at_point(self, point, attempts):
        host_batch = self.translate_host(point, attempts)
        guest_batch = self.rotate_guest(attempts)

        complexes = [
            self.create_new_complex(hcoords, gcoords)
            for hcoords, gcoords in zip(host_batch, guest_batch)
        ]

        return complexes

