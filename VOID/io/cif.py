from pymatgen.io.cif import CifParser, CifWriter


def read_cif(path, primitive=True):
    parser = CifParser(path)
    return parser.get_structures(primitive)[0]


def write_cif(path, structure):
    writer = CifWriter(structure)
    writer.write_file(path)
