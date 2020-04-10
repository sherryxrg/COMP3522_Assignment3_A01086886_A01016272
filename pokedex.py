"""
Facade UI that provides access to the poketriever module.
"""
import argparse
from pokeretriever.args_process import Request


class Pokedex:

    def __init__(self):
        pass

    def execute_request(self, request: Request):
        # process request
        request.process_pokedex_object()

    def cmd_requests(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('mode', type=str,
                            choices=['pokemon', 'ability', 'move'],
                            help="Mode application will be opened in")

        group = parser.add_mutually_exclusive_group(required=True)
        # todo: must have '.txt' extension
        group.add_argument('-if', '--inputfile',
                           help="File must have .txt extension.")
        # todo: id must be an int, and name must be str
        group.add_argument('-id', '--inputdata', type=int or str,
                           help="ID must be a digit, name must be a string.")

        parser.add_argument('-x', '--expanded',
                            action="store_true",
                            help="Only Pokemon queries support this mode. Default is False.")
        # todo: must have '.txt' extension
        parser.add_argument('-o', '--output', type=str,
                            help="File must have .txt extension.")

        # This parses all the arguments passed
        # through terminal/command line
        args = parser.parse_args()
        return args