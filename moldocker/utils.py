import numpy as np
from pymatgen.core.structure import Structure, Molecule, PeriodicSite


def join_structures(src, dst, validate_proximity=False):
    """Joins two pymatgen structures"""
    for site in src.sites:
        dst.append(
            species=site.species,
            coords=site.coords,
            coords_are_cartesian=True,
            validate_proximity=validate_proximity,
        )

    return dst


def get_molecule_structure_distances(
    joint_structure, length_substrate,
):
    """Gets the distances between the molecule and the substrate.

    Args:
        joint_struct (Structure): contains the molecule docked on
            the substrate.
        length_substrate (int): number of atoms of the substrate.
            As the code appends the molecules to the indices, we
            just need to split the joint structure into substrate
            and molecule using this index.
    """
    distance_matrix = joint_structure.distance_matrix[
        :length_substrate, length_substrate:
    ]

    return np.sum(np.min(distance_matrix, axis=0))


def get_loading(substrate, molecule, joint_structure):
    num_molecule_atoms = len(joint_structure) - len(substrate)
    return num_molecule_atoms // len(molecule)
