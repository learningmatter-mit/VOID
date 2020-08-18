import numpy as np
from pymatgen.core import Molecule, Structure

from .molecule import MoleculeTransformer
from VOID.utils.geometry import random_rotation_matrices


class Complex:
    def __init__(
        self, host, guest, add_transform=True
    ):
        """Constructor for host-guest pair. The `guest_transform` is useful to perform operations on the molecule. It performs all changes in place, meaning that the MoleculeTransformer has to have access to the reference of `self.guest` in order to be effective.

        Args:
            host (Structure)
            guest (Molecule)
            add_transform (bool): if True, create a MoleculeTransformer to apply
                operations to the guest
        """

        self.host = host
        self.guest = guest
        self.guest_transform = MoleculeTransformer(self.guest) if add_transform else None

    def __len__(self):
        return len(self.host) + len(self.guest)

    def copy(self):
        return Complex(self.host.copy(), self.guest.copy())

    @property
    def pose(self):
        species = self.host.species + self.guest.species
        coords = np.concatenate([self.host.cart_coords, self.guest.cart_coords], axis=0)
        host_props = self.host.site_properties.get("label", ["host"] * len(self.host))
        guest_props = self.guest.site_properties.get(
            "label", ["guest"] * len(self.guest)
        )
        props = {"label": host_props + guest_props}

        return Structure(
            species=species,
            coords=coords,
            coords_are_cartesian=True,
            lattice=self.host.lattice.matrix,
            site_properties=props,
        )

    @property
    def distance_matrix(self):
        """Returns the distance matrix between
            the host (rows) and the guest (columns).
        """
        return self.get_distance_matrix(structure="complex")

    def get_distance_matrix(self, structure="complex"):
        if structure == "complex":
            return self.host.lattice.get_all_distances(
                self.host.frac_coords, self.to_frac_coords(self.guest.cart_coords)
            )
        elif structure == "host":
            return self.host.distance_matrix
        elif structure == "guest":
            return self.host.lattice.get_all_distances(
                self.to_frac_coords(self.guest.cart_coords),
                self.to_frac_coords(self.guest.cart_coords),
            )
        else:
            raise ValueError("invalid structure name")

    def to_frac_coords(self, coords):
        return self.host.lattice.get_fractional_coords(coords.reshape(-1, 3)).reshape(
            coords.shape
        )
