# Examples and usage tutorial

The following examples are currently available in this repository:

1. [Docking a molecule to AFI zeolite](AFI): one molecule is docked to AFI using the Voronoi batch docker.
2. [Docking TMAda+ to CHA zeolite](CHA_TMada): one molecule is docked to CHA with Voronoi (sequential) and Monte Carlo dockers.
3. [Docking Diethylbenzenium cation (DEB+) into an acid UTL zeolite](Cation_Anion): One DEB+ molecule is docked to a UTL framework containing one Al atom, hence 4 acid sites. The minimmum cation-anion fitness ensures a close positioning of the docked molecule with respect to the acid sites of the host.
4. [Docking triethylamine to MOR zeolite](MOR_loading): several triethylamine molecules are docked to MOR zeolite with Voronoi batch docker.
5. [Docking benzene to MOF-5](MOF-5): several benzene molecules are docked to MOF-5 using the Voronoi batched docker. The MOF-5 structure was retrieved from the Cambridge Structural Database (ID [SAHYIK](https://www.ccdc.cam.ac.uk/structures/search?identifier=SAHYIK))
6. [Docking water to a Ni(111) surface](Ni111): one water molecule is docked to a Ni(111) surface using the Gaussian target fitness function. The Ni(111) surface structure was retrieved from the [Materials Project](https://materialsproject.org) (ID [mp-23](https://materialsproject.org/materials/mp-23/surfaces/[1,%201,%201]/cif))


Each example has a `job.sh` script file showing how to run the docker.
