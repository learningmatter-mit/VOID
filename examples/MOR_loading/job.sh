#!/bin/bash

# Runs until the zeolite is fully loaded with molecules
python3 ../../scripts/dock.py MOR.cif triethylamine.xyz -d batch -s voronoi_cluster -f min_distance --subdock
