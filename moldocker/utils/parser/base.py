import argparse


class Parser:
    DESCRIPTION = """moldocker: a package to dock molecules
        to materials.
    """

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            description=self.DESCRIPTION, add_help=False
        )

        self.add_main_kwargs()

    def get_module_parsers(self, module):
        return {cls.PARSER_NAME: cls.get_parser() for cls in module.__all__}

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

        self.add_extra_main_kwargs()

    def add_extra_main_kwargs(self):
        pass

    def get_parent_parsers(self, options):
        return [self.parser]

    def parse_args(self, args=None):
        options, _ = self.parser.parse_known_args(args)
        parent_parsers = self.get_parent_parsers(options)

        newparser = argparse.ArgumentParser(
            description=self.DESCRIPTION, add_help=True, parents=parent_parsers
        )
        return newparser.parse_args(args)
