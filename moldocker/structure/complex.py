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
        return utils.join_structures(self.guest, self.host)

    def get_guest_host_distance(self):
        """get distance between atoms from the guest and host"""
        return utils.get_molecule_structure_distances(self.pose, len(self.host))
