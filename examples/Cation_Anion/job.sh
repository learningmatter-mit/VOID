#!/bin/bash

# Runs until the first success is found  Also with Monte Carlo docking
echo "This example runs the docking of a DEB+ molecule into an Al-UTL zeolite framework"
echo ""
echo "If job fails to reach a final pose you can tune --threshold_catan, --threshold and --attempts parameters"
echo ""
echo "Running Monte Carlo docking"
echo ""
python3 ../../scripts/dock.py structure.cif DEB+.xyz -d mcsuccess -s random -f min_catan_distance -o mcdocked --threshold_catan 3.5 --threshold 1.5 --attempts 200000 
echo "Final pose save to mcdocked folder"

