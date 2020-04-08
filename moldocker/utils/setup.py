import os
import json
from pymatgen.core import Structure, Molecule
from moldocker import dockers, samplers, fitness


class SetupRun:
    def __init__(self, args):
        self.args = vars(args)

    def get_module_classes(self, module):
        return {cls.PARSER_NAME: cls for cls in module.__all__}

    def get_docker(self):
        classes = self.get_module_classes(dockers)
        cls = classes[self.args["docker"]]

        sampler = self.get_sampler()
        fitness = self.get_fitness()
        host, guest = self.get_structures()

        docker = cls(host, guest, sampler, fitness)

        return docker

    def get_subdocker(self):
        docker = self.get_docker()
        subdocker = dockers.Subdocker(docker, self.args["max_subdock"])
        return subdocker

    def get_sampler(self):
        classes = self.get_module_classes(samplers)
        cls = classes[self.args["sampler"]]
        return cls(**self.args)

    def get_fitness(self):
        classes = self.get_module_classes(fitness)
        cls = classes[self.args["fitness"]]
        return cls(**self.args)

    def get_structures(self):
        host_path = self.args["input"][0]
        guest_path = self.args["input"][1]

        host = Structure.from_file(host_path)
        guest = Molecule.from_file(guest_path)

        return host, guest

    def make_output(self):
        if not os.path.exists(self.args["output"]):
            os.mkdir(self.args["output"])

    def save_args(self):
        path = os.path.join(self.args["output"], "args.json")
        with open(path, "w") as f:
            json.dump(self.args, f, indent=4)
