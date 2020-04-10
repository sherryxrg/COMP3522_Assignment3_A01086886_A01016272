"""
Contains all classes for making pokedexObjects.
"""
import textwrap


class PokedexObject:

    def __init__(self, name: str, id_num: int):
        self.name = name
        self.id_num = id_num


class PokemonStat(PokedexObject):

    def __init__(self, name: str, id_num: int, is_battle_only: bool):
        """
        hit the url field inside Pokemon and get a stat
        :param name:
        :param id_num:
        :param is_battle_only:
        """
        super().__init__(name, id_num)
        self.is_battle_only = is_battle_only

    def __str__(self):
        return f"\n*--- Pokemon Stats ---*" \
               f"\nBattle Only: {self.is_battle_only}"


class PokemonAbility(PokedexObject):

    def __init__(self, name: str, id_num: int, generation: str,
                 effect: str, short_effect: str, pokemon: list):
        super().__init__(name, id_num)
        self.generation = generation
        self.effect = effect
        self.short_effect = short_effect
        self.pokemon = pokemon

    def __str__(self):
        return f"\n*--- Pokemon Ability ---*" \
               f"\n> NAME: {self.name}" \
               f"\n> ID: {self.id_num}" \
               f"\n> EFFECT: {textwrap.fill(self.effect, 80)}" \
               f"\n> SHORT EFFECT: {self.short_effect}" \
               f"\n> POKEMON: {self.pokemon, 80}"


class PokemonMove(PokedexObject):

    def __init__(self, name: str, id_num: int, generation: str,
                 accuracy: int, pp: int, power: int,
                 move_type: str, damage_class: str, short_effect: str):
        super().__init__(name, id_num)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.move_type = move_type
        self.damage_class = damage_class
        self.short_effect = short_effect

    def __str__(self):
        return f"\n*--- Pokemon Move ---*" \
               f"\n> NAME: {self.name}" \
               f"\n> ID: {self.id_num}" \
               f"\n> ACCURACY: {self.accuracy}" \
               f"\n> MOVE TYPE: {self.move_type}" \
               f"\n> EFFECT: {self.short_effect}"


class Pokemon(PokedexObject):

    def __init__(self, name: str, id_num: int, height: int, weight: int,
                 stats: PokemonStat, types: list, abilities: PokemonAbility,
                 moves: PokemonMove):
        super().__init__(name, id_num)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.moves = moves

    def __str__(self):
        return f"\n*--- Pokemon ---*" \
               f"\n> NAME: {self.name}" \
               f"\n> ID: {self.id_num}" \
               f"\n> STATS: {self.stats}" \
               f"\n> TYPES: {self.types}" \
               f"\n> ABILITIES: {self.abilities}" \
               f"\n> MOVES: {self.moves}"
