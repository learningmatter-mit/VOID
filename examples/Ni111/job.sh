#!/bin/bash

# Runs until the first success is found
echo "Running Monte Carlo docking of water on Ni(111)"
python3 ../../scripts/dock.py Ni111.cif water.xyz -d mcdocker -s random -f min_distance_target -o docked --target 1.6
