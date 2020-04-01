import numpy as np


MAX_SUBDOCK = 3


class Subdocker:
    """Useful to maximize the loading of a guest
        inside a host. Tries to put as many guests
        as possible inside the host
    """
    def __init__(
        self,
        host,
        guest,
        docker,
        sampler,
        scoring_fn,
        max_subdock=MAX_SUBDOCK
    ):
        self.host = host
        self.guest = guest
        self.docker = docker
        self.sampler = sampler
        self.scoring_fn = scoring_fn
        self.max_subdock = max_subdock

    def dock(self, host, guest, attempts):
        docker = self.docker(
            self.host,
            self.guest,
            self.sampler,
            self.scoring_fn
        )
        
        complexes = docker.dock(attempts)
        loading = 1

        complex_loading = {loading: complexes}
        while len(complexes) > 0:
            higher_loading = []

            for cpx in complexes[:self.max_subdock]:
                subdocker = self.docker(
                    cpx.pose,
                    self.guest,
                    self.sampler,
                    self.scoring_fn
                )
                
                higher_loading += subdocker.dock(attempts)

            higher_loading = self.rank_structures(higher_loading)



        




    
