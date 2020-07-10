import numpy as np
from typing import List
from pymatgen.core import Structure, Molecule

from moldocker.structure import Complex
from moldocker.object import ParseableObject


ATTEMPTS = 50


class Docker(ParseableObject):
    """Base class to dock a guest into a crystal"""

    PARSER_NAME = "base"
    HELP = "Base docker; does not implement any docking procedure"

    def __init__(self, host, guest, sampler, fitness, **kwargs):
        self.host = host
        self.guest = guest
        self.sampler = sampler
        self.fitness = fitness

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--attempts",
            type=int,
            help="maximum number of attempts to dock (default: %(default)s)",
            default=ATTEMPTS,
        )

    def copy(self):
        return self.__class__(
            self.host.copy(), self.guest.copy(), self.sampler, self.fitness
        )

    def new_host(self, newcoords=None):
        if newcoords is None:
            return self.host.copy()

        return Structure(
            species=self.host.species,
            coords=newcoords,
            lattice=self.host.lattice.matrix,
            coords_are_cartesian=True,
        )

    def new_guest(self, newcoords=None):
        if newcoords is None:
            return self.guest.copy()

        return Molecule(species=self.guest.species, coords=newcoords,)

    def create_new_complex(self, host_coords, guest_coords):
        return Complex(
            self.new_host(newcoords=host_coords),
            self.new_guest(newcoords=guest_coords),
            add_transform=False
        )

    def dock(self, attempts: int) -> List[Complex]:
        """Docks the guest into the host.
        """
        complexes = []
        for point in self.sampler.get_points(self.host):
            complexes += self.dock_at_point(point, attempts)

        complexes = self.rank_complexes(complexes)

        return complexes

    def dock_at_point(self, point, attempts):
        raise NotImplementedError

    def rank_complexes(self, complexes):
        scores = [self.fitness(cpx) for cpx in complexes]
        ranking = sorted(zip(complexes, scores), key=lambda x: x[1], reverse=True)

        return [cpx for cpx, fit in ranking if fit >= 0]
