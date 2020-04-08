import argparse
from moldocker import dockers, samplers, fitness


class Parser:
    DESCRIPTION = """moldocker: a package to dock molecules
        to materials.
    """

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            description=self.DESCRIPTION, add_help=False
        )

        self.add_main_kwargs()
        self.docker_opts = self.get_dockers_parsers()
        self.sampler_opts = self.get_samplers_parsers()
        self.fitness_opts = self.get_fitness_parsers()

    def get_module_parsers(self, module):
        return {cls.PARSER_NAME: cls.get_parser() for cls in module.__all__}

    def get_dockers_parsers(self):
        parsers = self.get_module_parsers(dockers)
        self.parser.add_argument(
            "-d",
            "--docker",
            type=str,
            help="Docker to be used",
            choices=list(parsers.keys()),
        )
        return parsers

    def get_samplers_parsers(self):
        parsers = self.get_module_parsers(samplers)
        self.parser.add_argument(
            "-s",
            "--sampler",
            type=str,
            help="Sampler to be used",
            choices=list(parsers.keys()),
        )
        return parsers

    def get_fitness_parsers(self):
        parsers = self.get_module_parsers(fitness)
        self.parser.add_argument(
            "-f",
            "--fitness",
            type=str,
            help="fitness function to be used",
            choices=list(parsers.keys()),
        )
        return parsers

    def add_main_kwargs(self):
        self.parser.add_argument(
            "input",
            type=str,
            nargs=2,
            help="Paths to input structures (host and guest)",
        )

        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Paths to output complexes (default: %(default)s)",
            default="docked",
        )

        self.parser.add_argument(
            "--subdock",
            help="If set, allow subdocking of molecules inside the structure (default: %(default)s)",
            default=False,
            action="store_true",
        )

    def parse_args(self, args=None):
        options, _ = self.parser.parse_known_args(args)
        parent_parsers = [
            self.parser,
            self.docker_opts[options.docker],
            self.sampler_opts[options.sampler],
            self.fitness_opts[options.fitness],
        ]

        if options.subdock:
            parent_parsers.append(self.docker_opts["subdock"],)

        newparser = argparse.ArgumentParser(
            description=self.DESCRIPTION, add_help=True, parents=parent_parsers
        )
        return newparser.parse_args(args)
