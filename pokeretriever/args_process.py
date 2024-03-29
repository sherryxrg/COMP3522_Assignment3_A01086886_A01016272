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

    async def api_call(self, poke_id, session: aiohttp.ClientSession, opt_url = None) -> dict:
        if opt_url is not None:
            api_url = opt_url + str(poke_id)
        else:
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

            # todo: parse lists - stats, types, abilities, moves
            if self.mode.lower() == 'pokemon':
                stats_dict = {}
                stats_list = response['stats']
                print(stats_list)
                for d in stats_list:
                    stats_dict[d['stat']['name']] = d['base_stat']

                type_list = []
                response_type = response['types']
                for d in response_type:
                    type_list.append(d['type']['name'])

                ability_list = []
                response_ability = response['abilities']
                for d in response_ability:
                    ability_list.append(d['ability']['name'])

                moves_dict = {}
                moves_list = response['moves']
                for d in moves_list:
                    moves_dict[d['move']['name']] = d['version_group_details'][0]['level_learned_at']

                if self.expanded:
                    # ability
                    async with aiohttp.ClientSession() as session:
                        a_url = [a['ability']['name'] for a in
                                 response_ability]
                        a_coroutines = [self.api_call(a, session,
                                                      opt_url='https://pokeapi.co/api/v2/ability/')
                                        for a in a_url]
                        a_responses = await asyncio.gather(*a_coroutines)
                        # print(a_responses)
                    # ability_list = a_responses
                    # a_obj_list = {}
                    # for i, e in enumerate(ability_list):
                    #     a_obj_list[e] = a_responses[i]

                    # stat
                    async with aiohttp.ClientSession() as session:
                        s_url = [s for s in stats_dict.keys()]
                        s_coroutines = [self.api_call(s, session,
                                                      opt_url='https://pokeapi.co/api/v2/stat/')
                                        for s in s_url]
                        s_responses = await asyncio.gather(*s_coroutines)
                        s_dict = {}
                        for x in s_url:
                            for y in s_responses:
                               stat = PokemonStat(x, 0, y['is_battle_only'])

                    # move
                    async with aiohttp.ClientSession() as session:
                        # for x in moves_dict.keys():
                        #     print(x)
                        m_url = [m for m in moves_dict.keys()]
                        m_coroutines = [self.api_call(m, session,
                                                      opt_url='https://pokeapi.co/api/v2/move/')
                                        for m in m_url]
                        m_responses = await asyncio.gather(*m_coroutines)
                        # print(m_responses)
                    # moves_dict = m_responses
                    print("THIS IS THE EXPANDED ABILITY RESPONSES:\n")
                    print(a_responses)
                    print("THIS IS THE EXPANDED STAT RESPONSES:\n")
                    print(s_responses)

                # do something with the key, value pair
                pokemon = Pokemon(response['name'],
                                  int(response['id']),
                                  int(response['height']),
                                  int(response['weight']),
                                  stats_dict,
                                  type_list,
                                  ability_list,  # now takes in an object
                                  moves_dict)
                self.pokedex.append(pokemon)
                # p_type = response['types']
                print(f">> GOT {self.mode}: {mode_name.upper()}, "
                      f"{pokemon.types} Pokemon!")

            if self.mode.lower() == 'ability':
                pokemon_list = []
                response_pokemon = response['pokemon']
                for d in response_pokemon:
                    pokemon_list.append(d['pokemon']['name'])

                effect = response['effect_entries']
                ability = PokemonAbility(response['name'],
                                         int(response['id']),
                                         response['generation'],
                                         effect[0]['effect'],
                                         effect[0]['short_effect'],
                                         pokemon_list)
                self.pokedex.append(ability)
                print(f">> GOT {self.mode}: {mode_name.upper()}! "
                      f"{ability.short_effect}")

            if self.mode.lower() == 'move':
                effect = response['effect_entries']
                move = PokemonMove(response['name'],
                                   int(response['id']),
                                   response['generation'],
                                   response['accuracy'], response['pp'],
                                   response['power'],
                                   response['type']['name'],
                                   response['damage_class'],
                                   effect[0]['short_effect'])
                self.pokedex.append(move)
                print(f">> GOT {self.mode}: {mode_name.upper()}! "
                      f"{move.short_effect}")

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
