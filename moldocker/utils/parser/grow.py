from .base import Parser
from moldocker import mcarlo, fitness


class GrowParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mcarlo_opts = self.get_mcarlo_parsers()
        self.fitness_opts = self.get_fitness_parsers()

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

    def get_mcarlo_parsers(self):
        parsers = self.get_module_parsers(mcarlo)
        self.parser.add_argument(
            "-m",
            "--mcarlo",
            type=str,
            help="Monte Carlo utility to be used",
            choices=list(parsers.keys()),
        )
        return parsers

    def add_extra_main_kwargs(self):
        pass

    def get_parent_parsers(self, options):
        parent_parsers = [
            self.parser,
            self.mcarlo_opts[options.mcarlo],
        ]

        return parent_parsers
