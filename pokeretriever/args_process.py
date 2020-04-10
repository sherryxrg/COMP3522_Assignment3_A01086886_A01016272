from pokeretriever.pokedex_classes import *
import ssl
import aiohttp
import asyncio


class Request:

    def __init__(self, mode: str,
                 expanded: bool, input_data,
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

        self.url = f"https://pokeapi.co/api/v2/{self.mode}/"
        self.pokedex = []

    def __str__(self):
        return f"\n== REQUEST OBJECT ==" \
               f"\nmode: {self.mode}" \
               f"\ndata: {self.input_data}" \
               f"\ninput file: {self.input_file}" \
               f"\nexpanded: {self.expanded}" \
               f"\noutput file: {self.output_file}"

    async def api_call(self, poke_id, session: aiohttp.ClientSession) -> dict:
        api_url = self.url + str(poke_id)
        response = await session.request(method="GET", url=api_url,
                                         ssl=ssl.SSLContext())
        json_response = await response.json()
        return json_response

    async def process_pokedex_object(self, poke_ids: list):
        """
        This function depicts the use of asyncio.gather to run multiple
        async coroutines concurrently. This allows us to execute multiple
        HTTP GET requests concurrently and save time.
        :param poke_ids: a list of int or str, representing name / id of either
        a Pokemon, Pokemon Move, Pokemon Ability, or Pokemon Stat
        """
        async with aiohttp.ClientSession() as session:
            list_urls = [p_id for p_id in poke_ids]
            coroutines = [self.api_call(my_url, session)
                          for my_url in list_urls]
            responses = await asyncio.gather(*coroutines)
            for response in responses:
                # print(response)
                mode_name = response['name']

                # todo: pokemon have 1-2 types
                if self.mode.lower() == 'pokemon':
                    pokemon = Pokemon(response['name'],
                                      int(response['id']),
                                      int(response['height']),
                                      int(response['weight']),
                                      response['stats'],
                                      response['types'],
                                      response['abilities'],
                                      response['moves'])
                    self.pokedex.append(pokemon)
                    p_type = response['types']
                    print(f">> GOT {self.mode}: {mode_name.upper()}, "
                          f"{p_type[0]['type']['name']} Pokemon!")

                if self.mode.lower() == 'ability':
                    effect = response['effect_entries']
                    ability = PokemonAbility(response['name'],
                                             int(response['id']),
                                             response['generation'],
                                             effect[0]['effect'],
                                             effect[0]['short_effect'],
                                             response['pokemon'])
                    self.pokedex.append(ability)
                    print(f">> GOT {self.mode}: {mode_name.upper()}! "
                          f"{effect[0]['short_effect']}")

                if self.mode.lower() == 'move':
                    effect = response['effect_entries']
                    move = PokemonMove(response['name'],
                                       int(response['id']),
                                       response['generation'],
                                       response['accuracy'], response['pp'],
                                       response['power'],
                                       response['type'],
                                       response['damage_class'],
                                       effect[0]['short_effect'])
                    self.pokedex.append(move)
                    print(f">> GOT {self.mode}: {mode_name.upper()}! "
                          f"{effect[0]['short_effect']}")

    def get_pokedex_object(self):
        """
        Does further processing on the dictionary to display it.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.process_pokedex_object(self.input_data))


def main():
    input_list = [1, 3, 5]
    r = Request('ability', input_list, False)
    r.get_pokedex_object()

    r1 = Request('pokemon', input_list, False)
    r1.get_pokedex_object()

    r2 = Request('move', input_list, False)
    r2.get_pokedex_object()

    for x in r2.pokedex:
        print(str(x))


if __name__ == '__main__':
    main()
