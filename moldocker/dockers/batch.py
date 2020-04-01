import numpy as np
from pymatgen.core import Structure, Molecule

from .base import Docker
from moldocker.structure import Complex
from moldocker.utils.geometry import random_rotation_matrices


class BatchDocker(Docker):
    def __init__(self, *args, scoring_fn, **kwargs):
        super().__init__(*args, **kwargs)
        self.scoring_fn = scoring_fn

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

    def dock_to_point(self, point, attempts):
        host_batch = self.translate_host(point, attempts)
        guest_batch = self.rotate_guest(attempts)

        dist_matrices = self.get_distance_matrices(host_batch, guest_batch)

        complexes = [
            self._complex_from_coords(hcoords, gcoords)
            for hcoords, gcoords, dm in zip(host_batch, guest_batch, dist_matrices)
            if self.scoring_fn(dm) > 0
        ]

        return complexes

    def _complex_from_coords(self, host_coords, guest_coords):
        
        new_host = Structure(
            species=self.host.species,
            coords=host_coords,
            lattice=self.host.lattice.matrix,
            coords_are_cartesian=True,
        )

        new_guest = Molecule(
            species=self.guest.species,
            coords=guest_coords,
        )

        return Complex(new_host, new_guest)

    def get_distance_matrices(self, host_batch, guest_batch):
        frac_host = self.to_frac_coords(host_batch)
        frac_guest = self.to_frac_coords(guest_batch)

        distance_matrices = [
            self.host.lattice.get_all_distances(f1, f2)
            for f1, f2 in zip(frac_host, frac_guest)
        ]

        return distance_matrices

    def to_frac_coords(self, coords):
        return self.host.lattice.get_fractional_coords(
            coords.reshape(-1, 3)
        ).reshape(coords.shape)
