# VOID: Voronoi Organic-Inorganic Docker

The VOID: Voronoi Organic-Inorganic Docker package (`VOID`) is a software designed to create conformations of molecules docked inside crystal structures. The package provides a library and scripts that include:
 - Sampling of the space using Voronoi diagrams
 - Geometrical fitness functions
 - Batched docking using tensorial operations
 - Monte Carlo docking

## Installation

This software requires the following packages:
- [numpy](https://numpy.org/)
- [pymatgen](https://pymatgen.org)
- [scikit-learn](https://scikit-learn.org/stable/)
- [networkx](https://networkx.github.io/)

```bash
conda upgrade conda
conda create -n VOID python=3.7 numpy networkx pymatgen>=2020.3.2 scikit-learn -c conda-forge
```

You need to activate the `VOID` environment to install the `VOID` package:

```bash
conda activate VOID
```

Finally, install the `VOID` package by running:

```bash
pip install .
```

### Zeo++ dependency

Zeo++ and its interface to pymatgen are required to use the Voronoi sampler. Please follow the instructions at the [pymatgen documentation](https://pymatgen.org/pymatgen.io.zeopp.html#zeo-installation-steps) to install both accordingly.

## Usage

### Command line
The simplest way to use the `VOID` package is to use the premade script `dock.py` (in the `scripts`) folder. As an example, we provide a molecule and a zeolite in [VOID/tests/files](VOID/tests/files). With `VOID` installed, you can dock the molecule to the zeolite using the following command:

```bash
dock.py VOID/tests/files/{AFI.cif,molecule.xyz} -o ~/Desktop/docked -d batch -s voronoi_cluster -f min_distance
```

This will dock the molecule contained in `molecule.xyz` to the zeolite in `AFI.cif` using the batch docker, Voronoi sampler with predefined number of clusters and a fitness function that considers the minimum distance between the host and the guest. All output files are saved in the folder `~/Desktop/docked`. All input files for crystals and molecules supported by pymatgen can be given as inputs, including [xyz, Gaussian inputs and outputs for molecules](https://pymatgen.org/pymatgen.core.structure.html#pymatgen.core.structure.IMolecule.from_file) and [CIF, VASP inputs and outputs, CSSR and others for crystals](https://pymatgen.org/pymatgen.core.structure.html#pymatgen.core.structure.IStructure.from_file).

For more information on the dockers, samplers and fitness functions available, run `dock.py --help`. Help on further commands are available once the choice of dockers, samplers and fitness functions are made, e.g. `dock.py -d batch -s voronoi_cluster -f min_distance --help`.

## Examples

Further examples can be seen in the [examples](examples/README.md) folder.

## Nomenclature

The nomenclature of the variables in this software follows (mostly) the [traditional molecular docking terminology](https://en.wikipedia.org/wiki/Docking_(molecular))
