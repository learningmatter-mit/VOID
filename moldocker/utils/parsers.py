import argparse


def get_main_parser():
    cmd_parser = argparse.ArgumentParser()

class DockerParser(argparse.ArgumentParser):
    DESCRIPTION = """moldocker: a package to dock molecules
        to materials.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            description=self.DESCRIPTION,
            **kwargs
        )

    def add_docker_arguments(self):

    def add_scoring_arguments(self):
        self.add_argument(
            "--min_distance",
            type=float,
            help="minimum distance in Angstrom from the guest to the host (default: %(default)s)",
            default=1.5,
        )
        self.add_argument(
            "--attempts",
            type=int,
            default=50,
            help="Number of attempts to try docking (default: %(default)s)",
        )
        self.add_argument(
            "--n_clusters", type=int, help="Maximum number of points to analyze", default=10
        )


