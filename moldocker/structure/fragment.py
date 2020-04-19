import random
from pymatgen.core import Molecule


class FragmentCreator:
    RADICAL_SPECIES = "X0+"
    NBR_RADIUS = 2

    def __init__(self, frag):
        """Create fragments from molecules to make them appropriate for
            substitution/functionalization methods.

        Args:
            frag (pymatgen.core.Molecule)
        """
        self.frag = frag

    def is_neighbor(self, atom, nbr):
        return nbr in self.frag.get_neighbors(atom, self.NBR_RADIUS)

    def is_species(self, atom, species):
        return atom.species_string == species

    def is_fragment_formatted(self):
        return self.is_species(self.frag[0], self.RADICAL_SPECIES) and self.is_neighbor(
            self.frag[0], self.frag[1]
        )

    def sample_terminal_atom(self):
        hydrogens = [at for at in self.frag if self.is_species(at, "H")]
        return random.sample(hydrogens, 1)[0]

    def create_radical(self, atom=None):
        if atom is None:
            atom = self.sample_terminal_atom()

        nearest_nbr = [
            nbr
            for nbr in self.frag.get_neighbors(atom, self.NBR_RADIUS)
            if not self.is_species(nbr, "H")
        ][0]

        self.frag.remove(atom)
        self.frag.remove(nearest_nbr)

        # insert the atoms again to reorder them
        self.frag.insert(0, self.RADICAL_SPECIES, atom.coords)
        self.frag.insert(1, nearest_nbr.species, nearest_nbr.coords)

        if not self.is_fragment_formatted():
            raise RuntimeError("Unknown error during formatting of fragment")

        return self.frag

    def get_fragment(self):
        if self.is_fragment_formatted():
            return self.frag

        return self.create_radical()
