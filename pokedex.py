"""
Facade UI that provides access to the poketriever module.
"""
import argparse
import textwrap
from pokeretriever.args_process import Request
from pokeretriever.pokedex_classes import *
from prettytable import PrettyTable


class Pokedex:

    def __init__(self):
        """
        Stores the pokedex from the request object.
        """
        self.pokedex_list = []

    def execute_request(self, request: Request):
        # process request -- populate request.pokedex
        request.get_pokedex_object()

        self.pokedex_list = request.pokedex
        # Done! -- print to console, and also write to file
        self._gen_output(request)

    def cmd_requests(self) -> Request:
        parser = argparse.ArgumentParser()
        parser.add_argument('mode', type=str,
                            choices=['pokemon', 'ability', 'move'],
                            help="Mode application will be opened in")

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-if', '--inputfile',
                           help="File must have .txt extension.")
        group.add_argument('-id', '--inputdata', action='append',
                           help="ID must be a digit, name must be a string.")
        parser.add_argument('-x', '--expanded',
                            action="store_true",
                            help="Only Pokemon queries support this mode. "
                                 "Default is False.")
        parser.add_argument('-o', '--output', type=str,
                            help="File must have .txt extension.")

        # This parses all the arguments passed
        # through terminal/command line
        args = parser.parse_args()

        # todo: might want to refactor this to another method !!
        # input_data varies based on input
        output = ""
        if args.output:
            output = args.output

        if args.inputfile:
            with open(args.inputfile, 'r') as f:
                words_list = f.read().split("\n")
                words_list.pop()

            input_data = words_list
            req = Request(args.mode, args.expanded, input_data,
                          output_file=output)
        else:
            input_data = args.inputdata
            req = Request(args.mode, args.expanded, input_data,
                          output_file=output)

        self.pokedex_list.append(req)
        return req

    def _gen_output(self, request: Request):
        """
        Request generates an output if the --output flag is on.
        Otherwise prints output to console.
        """
        # if output is true, also write to file as well
        print("\nrequest file: ", request.output_file)

        if request.output_file is not None:
            with open(f"{request.output_file}", 'w') as f:
                f.write("+======= Courtesy of Dr. Oaks' Lab =======+")
                for poke_obj in self.pokedex_list:
                    f.write(str(poke_obj))
                    f.write("\n")

        # otherwise just ouput to console:
        for poke_obj in self.pokedex_list:
            print(str(poke_obj))


def main():

    pkdx = Pokedex()

    req = pkdx.cmd_requests()
    pkdx.execute_request(req)


if __name__ == "__main__":
    main()
