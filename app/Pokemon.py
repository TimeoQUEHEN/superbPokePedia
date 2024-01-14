from app.PokeInteract import *

poke = PokeInteract()


class Pokemon:
    def __init__(self, name):
        pokemon = poke.get_poke(name=name)
        self.id = poke.get_poke_id(pokemon)
        self.species = poke.get_species(name=name)
        self.name = poke.get_poke_name(pokemon)
        self.french_name = poke.get_poke_lang_name(self.name)[4]['name']
        self.types = [type_p['type']['name'] for type_p in poke.get_poke_types(pokemon)]
        self.abilities = []
        self.hidden_ability = None
        for ability in poke.get_poke_ability(pokemon):
            if ability['is_hidden']:
                self.hidden_ability = ability['ability']
            else:
                self.abilities.append(ability['ability'])
        self.sprites = poke.get_poke_sprite(pokemon).values()
        self.xp = poke.get_poke_exp(pokemon)
        self.stats = poke.get_poke_stats(pokemon)
        self.hp = poke.get_poke_hp(pokemon)
        self.attack = poke.get_poke_attack(pokemon)
        self.defense = poke.get_poke_defense(pokemon)
        self.sp_attack = poke.get_poke_special_attack(pokemon)
        self.sp_defense = poke.get_poke_special_defense(pokemon)
        self.speed = poke.get_poke_speed(pokemon)
