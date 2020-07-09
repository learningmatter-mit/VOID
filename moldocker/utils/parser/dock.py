from .base import Parser
from moldocker import dockers, samplers, fitness, mcarlo


class DockParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docker_opts = self.get_dockers_parsers()
        self.sampler_opts = self.get_samplers_parsers()
        self.fitness_opts = self.get_fitness_parsers()

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

    def add_extra_main_kwargs(self):
        self.parser.add_argument(
            "--subdock",
            help="If set, allow subdocking of molecules inside the structure (default: %(default)s)",
            default=False,
            action="store_true",
        )

    def get_parent_parsers(self, options):
        parent_parsers = [
            self.parser,
            self.docker_opts[options.docker],
            self.sampler_opts[options.sampler],
            self.fitness_opts[options.fitness],
        ]

        if options.subdock:
            parent_parsers.append(self.docker_opts["subdock"],)

        return parent_parsers


class MonteCarloDockParser(DockParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docker_opts = self.get_dockers_parsers()
        self.fitness_opts = self.get_fitness_parsers()

    def get_samplers_parsers(self):
        return None

    def get_dockers_parsers(self):
        parsers = self.get_module_parsers(mcarlo)
        self.parser.add_argument(
            "-d",
            "--docker",
            type=str,
            help="Docker to be used",
            choices=list(parsers.keys()),
        )
        return parsers

    def get_parent_parsers(self, options):
        parent_parsers = [
            self.parser,
            self.docker_opts[options.docker],
            self.fitness_opts[options.fitness],
        ]

        if options.subdock:
            parent_parsers.append(self.docker_opts["subdock"],)

        return parent_parsers
