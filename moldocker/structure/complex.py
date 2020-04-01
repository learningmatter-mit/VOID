import numpy as np
from moldocker import utils
from pymatgen.core import Molecule, Structure


class Complex:
    def __init__(
        self, host, guest,
    ):
        """Constructor for host-guest pair.

        Args:
            host (Structure)
            guest (Molecule)
        """

        self.host = host
        self.guest = guest

    @property
    def pose(self):
        species = self.host.species + self.guest.species
        coords = np.concatenate([self.host.cart_coords, self.guest.cart_coords], axis=0)
        props = {
            "label": ["host"] * len(self.host) + ["guest"] * len(self.guest)
        }

        return Structure(
            species=species,
            coords=coords,
            coords_are_cartesian=True,
            lattice=self.host.lattice.matrix,
            site_properties=props
        )

    def __len__(self):
        return len(self.host) + len(self.guest)
