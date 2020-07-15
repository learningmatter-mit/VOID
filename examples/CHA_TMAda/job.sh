#!/bin/bash

# Runs until the first success is found
echo "Running Voronoi docking"
python3 ../../scripts/dock.py CHA.cif TMAda.xyz -d success -s voronoi_cluster -f min_distance -o vdocked

# Also with Monte Carlo docking
echo "Running Monte Carlo docking"
python3 ../../scripts/dock.py CHA.cif TMAda.xyz -d mcsuccess -s random -f min_distance -o mcdocked
