#!/bin/bash

# Runs until the first success is found
echo "Running Voronoi docking on MOF-5"
python3 ../../scripts/dock.py MOF-5.cif benzene.xyz -d batch -s voronoi_cluster -f min_distance -o docked --subdock --num_clusters 4
