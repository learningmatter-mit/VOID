import numpy as np

from pymatgen.core.sites import Site
from pymatgen.core import Lattice, Structure

from VOID.structure import Complex
from VOID.dockers.serial import SerialDocker
from VOID.dockers.mcdocker import MonteCarloDocker


class SuccessDocker(SerialDocker):
    PARSER_NAME = "success"
    HELP = "Docks guests to host until a successful docking is found"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dock_at_point(self, point, attempts):
        hcoords = self.translate_host(point)

        for trial in range(attempts):
            cpx = self.create_new_complex(
                host_coords=hcoords, guest_coords=self.rotate_guest()
            )

            if self.fitness(cpx) >= 0:
                print(f"{trial + 1} attempts to success")
                return [cpx]

        return []


class SuccessMonteCarloDocker(MonteCarloDocker):
    PARSER_NAME = "mcsuccess"
    HELP = (
        "Docks guests to host until a successful docking is found (Monte Carlo version)"
    )

    def dock(self, attempts):
        cpx = Complex(self.host.copy(), self.guest.copy())

        for trial in range(attempts):
            cpx = self.run(cpx, 1)

            if self.fitness(cpx) >= 0:
                print(f"{trial + 1} attempts to success")
                cpx = self.rescale(cpx)
                return [cpx]

        return []

    def rescale(complex):
        """Rescale the complex to the 0-1 range so results can be visualized in direct and xyz format.

        Args:
            complex (Complex): The host-guest complex object containing the host and guest molecules.

        Returns:
            Complex: The rescaled host-guest complex object.
        """
        lattice = complex.pose.lattice
        frac_coords = []
        species_list = []
        site_labels = []

        for site in complex.pose:
            site_labels.append(site.label)
            species_list.append(site.species)
            coords = (
                site.frac_coords
                if site.label == "host"
                else np.mod(site.frac_coords, 1.0)
            )
            frac_coords.append(coords)

        site_properties = {"label": site_labels}

        updated_structure = Structure(
            lattice, species_list, frac_coords, site_properties=site_properties
        )

        num_host_atoms = len(complex.host)

        species = updated_structure.species
        cart_coords = updated_structure.cart_coords

        # Update the host and guest with the rescaled 0-1 species and coordinates
        complex.host = Structure(
            lattice=complex.host.lattice,
            species=species[:num_host_atoms],
            coords=cart_coords[:num_host_atoms],
            coords_are_cartesian=True,
            site_properties=complex.host.site_properties,
        )

        complex.guest = Structure(
            lattice=complex.host.lattice,
            species=species[num_host_atoms:],
            coords=cart_coords[num_host_atoms:],
            coords_are_cartesian=True,
            site_properties=complex.guest.site_properties,
        )

        return complex
