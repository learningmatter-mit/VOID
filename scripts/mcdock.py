#!/usr/bin/env python
import os
import logging

from moldocker.utils.parser import MonteCarloDockParser
from moldocker.utils.setup import SetupMonteCarloRun
from moldocker.io.cif import write_cif


if __name__ == "__main__":
    # parse arguments
    parser = MonteCarloDockParser()
    args = parser.parse_args()

    setup = SetupMonteCarloRun(args)
    setup.make_output()

    if args.subdock:
        docker = setup.get_subdocker()
    else:
        docker = setup.get_docker()

    complexes = docker.dock(args.attempts)

    for idx, cpx in enumerate(complexes):
        outpath = os.path.join(args.output, "%04d.cif" % idx)
        write_cif(outpath, cpx.pose)

    setup.save_args()
