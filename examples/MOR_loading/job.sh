#!/bin/bash

# Runs until the first success is found
python3 ../../scripts/dock.py MOR.cif triethylamine.xyz -d batch -s voronoi_cluster -f min_distance --subdock
