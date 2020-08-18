import argparse


class ParseableObject:
    PARSER_NAME = "parse"
    HELP = "Default parseable object"

    def __init__(self):
        pass

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser(description=cls.HELP, add_help=False)
        cls.add_arguments(parser)
        return parser

    @staticmethod
    def add_arguments(parser):
        pass
