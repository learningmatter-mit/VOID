#!/usr/bin/env python
import logging
import os
from argparse import Namespace


if __name__ == "__main__":
    # parse arguments
    parser = parsers.get_main_parser()
    parsers.add_subparsers(parser)
    args = Namespace(**parser.parse_args())

    # create docker, sampler and scoring
    docker, sampler, scoring = setup_run(args)

    # load host/guest
    host, guest = load_structures(args)

    complexes = docker.dock(args.attempts)
    to_subdock = complexes[:args.max_subdock]
    while len(to_subdock) > 0:

    



