import argparse
import ssl
import aiohttp
import asyncio


class Request:

    def __init__(self, mode: str, input_data: str,
                 expanded: bool,
                 input_file=None, output_file=None):
        """
        Also stores a list of pokedex objects in self.pokedex
        :param mode:
        :param input_data:
        :param expanded:
        :param input_file:
        :param output_file:
        """
        self.mode = mode
        self.input_data = input_data
        self.expanded = expanded
        self.input_file = input_file
        self.output_file = output_file

        self.url = "https://pokeapi.co/api/v2/"
        self.pokedex = []

    def __str__(self):
        return f"\n== REQUEST OBJECT ==" \
               f"\nmode: {self.mode}" \
               f"\ndata: {self.input_data}" \
               f"\ninput file: {self.input_file}" \
               f"\nexpanded: {self.expanded}" \
               f"\noutput file: {self.output_file}"

    async def get_pokedex_object(self, pokedex_obj, session: aiohttp.ClientSession) -> dict:
        url = self.url + str(pokedex_obj)
        response = await session.request(method="GET", url=url,
                                         ssl=ssl.SSLContext())
        json_response = await response.json()
        return json_response

    async def _process_pokedex_object(self, objects: list):
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
                print(response)
                # effect = response['effect_entries']
                # ability = Ability(response['name'], int(response['id']),
                #                   response['generation'], effect[0]['effect'], effect[0]['short_effect'], response['pokemon'])
                # self.abilities.append(ability)
                # ability_name = response['name']
                # print(f"Ability: {ability_name.upper()}! {effect[0]['short_effect']}")


def main():
    pass


if __name__ == '__main__':
    main()
