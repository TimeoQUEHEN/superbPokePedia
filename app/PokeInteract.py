#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citées pourra engager des poursuites.

import requests


# # TODO Docstring # #

class PokeInteract:
    def __init__(self):
        self.url = "https://pokeapi.co/api/v2/"

    def all_poke(self):
        limit = requests.get(f"{self.url}pokemon").json()['count']
        return requests.get(f"{self.url}pokemon?limit={limit}").json()

    def all_species(self):
        limit = requests.get(f"{self.url}pokemon-species").json()['count']
        return requests.get(f"{self.url}pokemon-species?limit={limit}").json()

    def get_poke(self, name):
        return requests.get(f"{self.url}pokemon/{name}").json()

    def get_type(self, name):
        return requests.get(f"{self.url}type/{name}").json()

    def get_ability(self, name):
        return requests.get(f"{self.url}ability/{name}").json()

    def get_move(self, name):
        return requests.get(f"{self.url}move/{name}").json()

    def get_item(self, name):
        return requests.get(f"{self.url}item/{name}").json()

    def get_region(self, name):
        return requests.get(f"{self.url}region/{name}").json()

    def get_species(self, name):
        poke = self.get_poke(name)
        return requests.get(poke['species']['url']).json()

    @staticmethod
    def get_poke_name(poke: dict) -> str:
        return poke['name']

    @staticmethod
    def get_poke_lang_name(poke: str) -> dict:
        return requests.get("https://pokeapi.co/api/v2/pokemon-species/"+poke).json()['names']

    @staticmethod
    def get_poke_ability(poke: dict) -> list:
        return poke['abilities']

    @staticmethod
    def get_poke_id(poke: dict) -> int:
        return poke['id']

    @staticmethod
    def get_poke_exp(poke: dict) -> int:
        return poke['base_experience']

    @staticmethod
    def get_poke_sprite(poke: dict) -> dict:
        if poke['sprites']['front_female']:
            return {'male': poke['sprites']['front_default'],
                    'female': poke['sprites']['front_female'],
                    'shiny': poke['sprites']['front_shiny'],
                    'shiny_female': poke['sprites']['front_shiny_female']}
        else:
            return {'male': poke['sprites']['front_default'],
                    'female': None,
                    'shiny': poke['sprites']['front_shiny'],
                    'shiny_female': None
                    }

    @staticmethod
    def get_poke_stats(poke: dict) -> list:
        return poke['stats']

    @staticmethod
    def get_poke_types(poke: dict) -> list:
        return poke['types']

    @staticmethod
    def get_poke_hp(poke: dict):
        return PokeInteract.get_poke_stats(poke)[0]['base_stat']

    @staticmethod
    def get_poke_attack(poke: dict):
        return PokeInteract.get_poke_stats(poke)[1]['base_stat']

    @staticmethod
    def get_poke_defense(poke: dict):
        return PokeInteract.get_poke_stats(poke)[2]['base_stat']

    @staticmethod
    def get_poke_special_attack(poke: dict):
        return PokeInteract.get_poke_stats(poke)[3]['base_stat']

    @staticmethod
    def get_poke_special_defense(poke: dict):
        return PokeInteract.get_poke_stats(poke)[4]['base_stat']

    @staticmethod
    def get_poke_speed(poke: dict):
        return PokeInteract.get_poke_stats(poke)[5]['base_stat']

    @staticmethod
    def get_poke_evolution_chain(poke: dict):
        evolution = []
        dico = requests.get(requests.get(poke["species"]["url"]).json()["evolution_chain"]["url"]).json()["chain"]
        do = True
        while (do):
            evolution.append(requests.get("https://pokeapi.co/api/v2/pokemon/"+dico["species"]["name"]).json())
            if len(dico["evolves_to"]) == 0:
                do = False
            else:
                dico = dico["evolves_to"][0]
        return evolution
