import argparse
import ssl
import aiohttp
import asyncio


class Request:

    def __init__(self, mode: str, input_data: str,
                 expanded: bool,
                 input_file=None, output_file=None):
        self.mode = mode
        self.input_data = input_data
        self.expanded = expanded
        self.input_file = input_file
        self.output_file = output_file

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
                pass
                # effect = response['effect_entries']
                # ability = Ability(response['name'], int(response['id']),
                #                   response['generation'], effect[0]['effect'], effect[0]['short_effect'], response['pokemon'])
                # self.abilities.append(ability)
                # ability_name = response['name']
                # print(f"Ability: {ability_name.upper()}! {effect[0]['short_effect']}")



# class ProcessRequest:
#
#     def __init__(self):
#         """
#         Contains the root url for getting pokemon moves.
#         An instance of this class contains a list that holds
#         the moves it has processed.
#
#         moves stores a list of PokemonMove objects.
#         """
#         # url needs /pokemon /move OR /ability
#         self.url = "https://pokeapi.co/api/v2/"
#         self.pokedex = []
#
#     async def get_pokedex_object(self, pokedex_obj, session: aiohttp.ClientSession) -> dict:
#         url = self.url + str(pokedex_obj)
#         response = await session.request(method="GET", url=url,
#                                          ssl=ssl.SSLContext())
#         json_response = await response.json()
#         return json_response
#
#     async def process_pokedex_object(self, objects: list):
#         """
#         This function depicts the use of asyncio.gather to run multiple
#         async coroutines concurrently. This allows us to execute multiple
#         HTTP GET requests concurrently and save time.
#         :param objects: a list of int or str, a list of pokemon ability id/names
#         """
#         async with aiohttp.ClientSession() as session:
#             list_urls = [obj for obj in objects]
#             coroutines = [self.get_pokedex_object(my_url, session) for my_url
#                           in list_urls]
#             responses = await asyncio.gather(*coroutines)
#             for response in responses:
#                 pass
#                 # effect = response['effect_entries']
#                 # ability = Ability(response['name'], int(response['id']),
#                 #                   response['generation'], effect[0]['effect'], effect[0]['short_effect'], response['pokemon'])
#                 # self.abilities.append(ability)
#                 # ability_name = response['name']
#                 # print(f"Ability: {ability_name.upper()}! {effect[0]['short_effect']}")


def main():
    pass
    # cmd_args = cmd_requests()
    # if cmd_args.inputfile:
    #     input_data = cmd_args.inputfile
    # else:
    #     input_data = cmd_args.inputdata
    #
    # # args are parsed into an instance of Request class
    # req = Request(cmd_args.mode, input_data, cmd_args.expanded)
    #
    # # prints out command line arguments
    # temp = vars(req)
    # for item in temp:
    #     print(item, ':', temp[item])


if __name__ == '__main__':
    main()
