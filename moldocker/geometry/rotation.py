import numpy as np
import math


def rotation_matrix(axis, theta):
    """ Return the rotation matrix associated with
 	counterclockwise rotation about
    	the given axis by theta radians.
        From https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
    """

    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )


def random_rotation_matrices(size):
    assert type(size) == int and size > 0

    if size == 1:
        return rotation_matrix(
            axis=np.random.randn(3), theta=(2 * np.pi * np.random.rand(1)[0])
        )

    return np.stack(
        [
            rotation_matrix(
                axis=np.random.randn(3), theta=(2 * np.pi * np.random.rand(1)[0])
            )
            for _ in range(size)
        ]
    )
