from app.PokeInteract import *

poke = PokeInteract


class Pokemon:
    def __init__(self, name):
        pokemon = poke().get_poke(name=name)
        self.id = poke.get_poke_id(pokemon)
        self.name = poke.get_poke_name(pokemon)
        self.xp = poke.get_poke_exp(pokemon)
        self.abilities = poke.get_poke_ability(poke)  # TODO : correct error
        self.sprites = poke.get_poke_sprite(pokemon)
        self.stats = poke.get_poke_stats(pokemon)
        self.types = poke.get_poke_types(pokemon)
