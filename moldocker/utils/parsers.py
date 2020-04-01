import argparse


def get_main_parser():
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument(
        "--min_distance",
        type=float,
        help="minimum distance in Angstrom from the guest to the host (default: %(default)s)",
        default=1.5,
    )
    cmd_parser.add_argument(
        "--attempts",
        type=int,
        default=50,
        help="Number of attempts to try docking (default: %(default)s)",
    )
    cmd_parser.add_argument(
        "--n_clusters", type=int, help="Maximum number of points to analyze", default=10
    )
    cmd_parser.add_argument(
        "--cutoff",
        type=float,
        default=5.0,
        help="Cutoff radius of local environment (default: %(default)s)",
    )
    cmd_parser.add_argument(
        "--trainable_gauss",
        action="store_true",
        help="If set, sets gaussians as learnable parameters (default: False)",
    )

    return cmd_parser
