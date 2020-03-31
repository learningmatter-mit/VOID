import numpy as np
from moldocker import utils


class Docker:
    """Base class to dock a guest into a crystal"""

    def __init__(
        self,
        host,
        guest,
        sampler,
        **kwargs
    ):
        self.host = host
        self.guest = guest
        self.sampler = sampler

    def rotate_guest(self, theta=None, axis=None):
        guest = self.guest.copy()

        if theta is None:
            theta = 2 * np.pi * np.random.rand(1)[0]

        if axis is None:
            axis = np.random.rand(3)

        guest.rotate_sites(theta=theta, axis=axis)

        return guest

    def translate_host(self, coords):
        """Translates all nodes of the host to the given coords.

        Args:
            coords (np.array): (3, ) array with cartesian coordinates.
        """

        host = self.host.copy()
        host.translate_sites(
            range(len(self.host)),
            -coords,
            frac_coords=False
        )

        return host

    def dock(self, attempts):
        """Docks the guest into the host.
        """

        poses = []
        for point in self.sampler.get_points(self.host):
            poses += self.dock_to_point(point, attempts)

        return poses

    def dock_to_point(self, point, attempts):
        subst = self.translate_host(point)

        poses = []
        for _ in range(attempts):
            mol = self.rotate_guest()

            try:
                docked = utils.join_structures(
                    mol,
                    subst,
                    validate_proximity=True
                )
                poses.append(docked)

            except ValueError:
                pass

        return poses

    def copy(self):
        return self.__class__(
            self.host.copy(),
            self.guest.copy(),
            self.sampler
        )

    def increase_loading(self, structures, attempts):
        high_loading_structs = []
        for struct in tqdm(
            structures,
            'increasing the loading of the given structures'
        ):
            subdocker = self.copy(host=struct)
            subdocked_structs = subdocker.dock(attempts)
            high_loading_structs += subdocked_structs

        return high_loading_structs
    

