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

    def cmd_requests(self) -> Request:
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
                            help="Only Pokemon queries support this mode. "
                                 "Default is False.")

        # todo: must have '.txt' extension
        parser.add_argument('-o', '--output', type=str,
                            help="File must have .txt extension.")

        # This parses all the arguments passed
        # through terminal/command line
        args = parser.parse_args()
        # return args

        # input_data varies based on input
        if args.inputfile:
            input_data = args.inputfile
        else:
            input_data = args.inputdata

        # make Request object
        req = Request(args.mode, input_data, args.expanded)
        return req

    def gen_output(self, file_name):
        with open(file_name, 'w') as f:
            for item in self.daily_transactions:
                f.write(f"Order {item[0]}, Item {item[1]}, "
                        f"Product ID {item[2]}, Name '{item[3]}', "
                        f"Quantity {item[4]}")
                f.write("\n")


def main():

    pkdx = Pokedex()
    req = pkdx.cmd_requests()
    print(str(req))


if __name__ == "__main__":
    main()
