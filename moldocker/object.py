class ParseableObject:
    PARSER_NAME = "parse"
    HELP = "Default parseable object"

    def __init__(self):
        pass

    def add_parser(self, subparser):
        parser = subparser.add_parser(self.PARSER_NAME, help=self.HELP)
        self.add_arguments(parser)

    def add_arguments(self, parser):
        pass
