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

If you are installing VOID in a Python environment (> Python 3.6) and encounter problems when compiling Zeo++, please refer below to [Compiling Zeo++ in Python >3.6 Environments](#compiling-zeo) for a solution.

### Zeo++ dependency

Zeo++ and its interface to pymatgen are required to use the Voronoi sampler. The following instructions for their installation are based off the original instructions at the [pymatgen documentation](https://pymatgen.org/pymatgen.io.zeopp.html#zeo-installation-steps). 

The original code retrieval with  `svn checkout –username anonsvn https://code.lbl.gov/svn/voro/trunk` (password anonsvn) no longer works. Instead, we suggest using these mirrors for [Voro++](https://github.com/chr1shr/voro) and [Zeo++](https://github.com/richardjgowers/zeoplusplus):

```bash
git clone https://github.com/chr1shr/voro.git
git clone https://github.com/richardjgowers/zeoplusplus.git
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

If you have problems compiling this library, please try contacting the Zeo++ developers. We do not offer support for compilation of Zeo++, Voro++ or other dependencies.

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

A new feature has recently been introduced that enables docking based on the acid site positions in the zeolite framework and the cation indexes on host molecules using a modified Monte Carlo algorithm. One can specify the maximum allowed distance between cation and acid sites in Amstrongs, as well as their corresponding indexes in the final structure, with the following command

```bash
python3 ../../scripts/dock.py structure.cif molecule.xyz -d mcsuccess -s random -f min_catan_distance -o ~/Desktop/mcdocked --threshold_catan 3 --cation_indexes 1 --acid_sites 2,3,4,5
```

## Examples

Further examples can be seen in the [examples](examples/README.md) folder.

<a id="compiling-zeo"></a>
## Compiling Zeo++ in Python > 3.6 Environments

Open the file located at:

```bash
~/{your_environment}/lib/python3.9/site-packages/Cython/Compiler/Main.py
```

Navigate to line 72 and change:

```bash
language_level = None
```

to

```bash
language_level = 3
```

Save and close the file.

After making this change, you should be able to continue with the installation steps described above without any issues.

```bash
 59 class Context(object):
 60     #  This class encapsulates the context needed for compiling
 61     #  one or more Cython implementation files along with their
 62     #  associated and imported declaration files. It includes
 63     #  the root of the module import namespace and the list
 64     #  of directories to search for include files.
 65     #
 66     #  modules               {string : ModuleScope}
 67     #  include_directories   [string]
 68     #  future_directives     [object]
 69     #  language_level        int     currently 2 or 3 for Python 2/3
 70 
 71     cython_scope = None
 72     language_level = 3  # warn when not set but default to Py2 --> change None to 3
```


## Nomenclature

The nomenclature of the variables in this software follows (mostly) the [traditional molecular docking terminology](https://en.wikipedia.org/wiki/Docking_(molecular))

## Citing

The publication describing the algorithm and the software is the following:


D. Schwalbe-Koda and R. Gómez-Bombarelli. _J. Phys. Chem. C_ **125** (5), 3009–3017 (2021). DOI [10.1021/acs.jpcc.0c10108](https://doi.org/10.1021/acs.jpcc.0c10108)

If you use this software, please cite the paper above. The bibtex for the citation is the following:

```
@article{schwalbe2021supramolecular,
  title={Supramolecular recognition in crystalline nanocavities through Monte Carlo and Voronoi network algorithms},
  author={Schwalbe-Koda, Daniel and G{\'o}mez-Bombarelli, Rafael},
  journal={The Journal of Physical Chemistry C},
  volume={125},
  number={5},
  pages={3009--3017},
  year={2021},
  publisher={ACS Publications}
}
```
