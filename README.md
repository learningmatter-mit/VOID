# Molecular Docking Tool

The Molecular Docking Tool (`moldocker`) is a software designed to create conformations of molecules docked inside crystal structures. The package provides a library and scripts that include:
 - Sampling of the space using Voronoi diagrams
 - Geometrical fitness functions
 - Batched docking using tensorial operations

## Installation

This software requires the following packages:
- [numpy](https://numpy.org/)
- [pymatgen](https://pymatgen.org)
- [scikit-learn](https://scikit-learn.org/stable/)

```bash
conda upgrade conda
conda create -n moldocker python=3.7 pymatgen>=2020.3.2 scikit-learn -c conda-forge
```

You need to activate the `moldocker` environment to install the `moldocker` package:

```bash
conda activate moldocker
```

Finally, install the `moldocker` package by running:

```bash
pip install .
```

### Zeo++ dependency

Zeo++ and its interface to pymatgen are required to use the Voronoi sampler. Please follow the instructions in the [pymatgen documentation](https://pymatgen.org/pymatgen.io.zeopp.html#zeo-installation-steps) to install both accordingly.

## Usage

### Command line
The simplest way to use the `moldocker` package is to use the premade scripts (in the `scripts`) folder. As an example, we provide a molecule and a zeolite in [moldocker/tests/files](moldocker/tests/files). With `moldocker` installed, you can dock the molecule to the zeolite using the following command:

```bash
dock.py moldocker/tests/files/{AFI.cif,molecule.xyz} -o ~/Desktop/dock -d batch -s voronoi_cluster -f min_distance
```

This will dock the molecule contained in `molecule.xyz` to the zeolite in `AFI.cif` using the batch docker, Voronoi sampler with predefined number of clusters and a fitness function that considers the minimum distance between the host and the guest. All output files are saved in the folder `~/Desktop/dock`.

## Nomenclature

The nomenclature of the variables in this software follows (mostly) the [traditional molecular docking terminology](https://en.wikipedia.org/wiki/Docking_(molecular))
