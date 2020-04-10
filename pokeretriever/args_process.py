import argparse
import ssl
import aiohttp
import asyncio


class ProcessRequest:

    def __init__(self):
        """
        Contains the root url for getting pokemon moves.
        An instance of this class contains a list that holds
        the moves it has processed.

        moves stores a list of PokemonMove objects.
        """
        # url needs /pokemon /move OR /ability
        self.url = "https://pokeapi.co/api/v2/"
        self.pokedex = []

    async def get_pokedex_object(self, pokedex_obj, session: aiohttp.ClientSession) -> dict:
        url = self.url + str(pokedex_obj)
        response = await session.request(method="GET", url=url,
                                         ssl=ssl.SSLContext())
        json_response = await response.json()
        return json_response

    async def process_pokedex_object(self, objects: list):
        """
        This function depicts the use of asyncio.gather to run multiple
        async coroutines concurrently. This allows us to execute multiple
        HTTP GET requests concurrently and save time.
        :param objects: a list of int or str, a list of pokemon ability id/names
        """
        async with aiohttp.ClientSession() as session:
            list_urls = [obj for obj in objects]
            coroutines = [self.get_pokedex_object(my_url, session) for my_url
                          in list_urls]
            responses = await asyncio.gather(*coroutines)
            for response in responses:
                # effect = response['effect_entries']
                # ability = Ability(response['name'], int(response['id']),
                #                   response['generation'], effect[0]['effect'], effect[0]['short_effect'], response['pokemon'])
                # self.abilities.append(ability)
                # ability_name = response['name']
                # print(f"Ability: {ability_name.upper()}! {effect[0]['short_effect']}")

                class Request:

                    def __init__(self, mode: str, input_data: str,
                                 expanded: bool,
                                 input_file=None, output_file=None):
                        self.mode = mode
                        self.input_data = input_data
                        self.expanded = expanded
                        self.input_file = input_file
                        self.output_file = output_file

                def cmd_requests():
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

                def main():
                    cmd_args = cmd_requests()
                    if cmd_args.inputfile:
                        input_data = cmd_args.inputfile
                    else:
                        input_data = cmd_args.inputdata

                    # args are parsed into an instance of Request class
                    req = Request(cmd_args.mode, input_data, cmd_args.expanded)

                    # prints out command line arguments
                    temp = vars(req)
                    for item in temp:
                        print(item, ':', temp[item])

                if __name__ == '__main__':
                    main()