from .base import Docker
from ..geometry.rotation import random_rotation_matrices


class BatchDocker(Docker):
    def rotate_guest(self, attempts):
        # (N, num_atoms, 3) matrix
        coords = np.repeat(self.guest.coords[None, ...], attempts, axis=0)

        # (N, 3, 3) matrix
        rotation = geometry.random_rotation_matrices(attempts)

        # (N, num_atoms, 3) matrix
        return np.matmul(coords, rotation.swapaxes(-1, -2))

    def translate_host(self, point, attempts):
        """Translates all nodes of the host to the given coords.

        Args:
            coords (np.array): (3, ) array with cartesian coordinates.
        """
        
        translated = self.host.cart_coords - point

        return np.repeat(translated[None, ...], attempts, axis=0)

    def dock_to_point(self, point, attempts):
        host = self.translate_host(point, attempts)
        guest = self.rotate_guest(attempts)

        poses = []
        for _ in range(attempts):
            mol = self.rotate_guest()

            try:
                docked = zeoutils.join_structures(
                    mol,
                    subst,
                    validate_proximity=True
                )
                poses.append(docked)

            except ValueError:
                pass

        return poses
