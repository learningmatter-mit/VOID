import numpy as np


MAX_SUBDOCK = 1


class Subdocker:
    """Useful to maximize the loading of a guest
        inside a host. Tries to put as many guests
        as possible inside the host
    """

    def __init__(self, docker, max_subdock=MAX_SUBDOCK):
        self.docker = docker
        self.max_subdock = max_subdock

    def dock(self, attempts):
        complexes = self.docker.dock(attempts)

        # loading is the number of guests inside the host
        loading = 1
        complex_loading = {}
        while len(complexes) > 0:
            complex_loading = {loading: complexes}
            higher_loading = []

            for cpx in complexes[:self.max_subdock]:
                subdocker = self.docker.copy()
                subdocker.host = cpx.pose
                higher_loading += subdocker.dock(attempts)

            complexes = self.docker.rank_complexes(higher_loading)
            loading += 1

        return complex_loading
