from moldocker import dockers, samplers, scoring


class Parser:
    DESCRIPTION = """moldocker: a package to dock molecules
        to materials.
    """

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(description=self.DESCRIPTION)

    def add_module_parsers(self, module, subparser):
        for cls in module.__all__:
            cls.add_parser(subparser)

    def add_dockers_subparser(self):
        subparser = self.parser.add_subparser(
            dest="docker", description="docker to be used"
        )
        self.add_module_parsers(dockers, subparser)

    def add_samplers_subparser(self):
        subparser = self.parser.add_subparser(
            dest="sampler", description="sampler to be used"
        )
        self.add_module_parsers(samplers, subparser)

    def add_scoring_subparser(self):
        subparser = self.parser.add_subparser(
            dest="scoring", description="scoring function to be used"
        )
        self.add_module_parsers(scoring, subparser)
