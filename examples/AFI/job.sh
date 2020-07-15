#!/bin/bash

python3 ../../scripts/dock.py AFI.cif molecule.xyz -d batch -s voronoi_cluster -f min_distance --threshold 1.8
