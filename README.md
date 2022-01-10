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
conda create --name VOID python=3.6.8 cython=0.29.5
```

You need to activate the `VOID` environment to install the dependencies for the `VOID` package and the package itself:

```bash
conda activate VOID
```

### Zeo++ dependency

Zeo++ and its interface to pymatgen are required to use the Voronoi sampler. The following instructions for their installation are based off the original instructions at the [pymatgen documentation](https://pymatgen.org/pymatgen.io.zeopp.html#zeo-installation-steps). 

The original code retrieval with  `svn checkout –username anonsvn https://code.lbl.gov/svn/voro/trunk` (password anonsvn) no longer works. Instead, use these repositories for [Voro++](https://github.com/chr1shr/voro) and [Zeo++](https://github.com/richardjgowers/zeoplusplus). 

```bash
git clone <insert HTTPS link>
```

Please note that there may be differences between the Zeo++ code in the Github repository and the stable version available for download in [this link](http://www.maciejharanczyk.info/Zeopp/). 

After retrieving the code, make the following edits to the Makefiles and config.mk files to point the code towards the correct directory paths (reading all the Makefiles and config.mk files in both packages is highly recommended for understanding of the installation process).

Add `-fPIC` to CFLAGS in `config.mk` in the Voro++ directory. Also, if you do not have permissions to access the default `PREFIX` path, change it to your desired directory.

Run these commands:

```bash
make
make install
```

You should notice the creation of several folders in the `PREFIX` directory you specified earlier. Edit the Makefile in the Zeo++ directory to include the correct paths in `VOROINCLDIR` and `VOROLINKDIR`. 

Run `make dylib` within the Zeo++ directory.

Navigate to `cython_wrapper/` in the Zeo++ directory and edit `setup_alt.py` to point the variables `includedirs` and `libdirs` to the correct Voro++ directory. Run `python setup_alt.py develop` to install Zeo++ python bindings.

If you have problems compiling this library, please try contacting the Zeo++ developers.

Finally, install the `VOID` package by navigating to the VOID directory and running:

```bash
pip install .
```

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
