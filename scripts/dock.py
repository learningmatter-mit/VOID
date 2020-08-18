#!/usr/bin/env python
import os
import logging

from VOID.utils.parser import DockParser
from VOID.utils.setup import SetupRun
from VOID.io.cif import write_cif


if __name__ == "__main__":
    # parse arguments
    parser = DockParser()
    args = parser.parse_args()

    setup = SetupRun(args)
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
