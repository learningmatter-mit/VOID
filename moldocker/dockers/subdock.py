import numpy as np

from moldocker.object import ParseableObject


MAX_SUBDOCK = 1


class Subdocker(ParseableObject):
    """Useful to maximize the loading of a guest
        inside a host. Tries to put as many guests
        as possible inside the host
    """

    PARSER_NAME = "subdock"
    HELP = "Docks recursively until the host is completely filled with guests"

    def __init__(self, docker, max_subdock=MAX_SUBDOCK):
        self.docker = docker
        self.max_subdock = max_subdock

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--max_subdock",
            type=int,
            help="maximum number of complexes to attempt subdocking (default: %(default)s)",
            default=MAX_SUBDOCK,
        )

    def dock(self, attempts):
        complexes = self.docker.dock(attempts)

        # loading is the number of guests inside the host
        loading = 1
        complex_loading = {}
        while len(complexes) > 0:
            complex_loading = {loading: complexes}
            higher_loading = []

            for cpx in complexes[: self.max_subdock]:
                subdocker = self.docker.copy()
                subdocker.host = cpx.pose
                higher_loading += subdocker.dock(attempts)

            complexes = self.docker.rank_complexes(higher_loading)
            loading += 1

        # TODO: make loading compatible with other dockers
        # right now, dock returns a list of complexes
        complexes = [subitem for item in complex_loading.values() for subitem in item]
        return complexes
