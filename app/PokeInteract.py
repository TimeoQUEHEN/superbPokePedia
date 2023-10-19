#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

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
    def get_poke_ability(poke) -> list:
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
                    'shiny': poke['sprites']['front_shiny']}

    @staticmethod
    def get_poke_stats(poke: dict):
        return poke['stats']
    # TODO repare

    @staticmethod
    def get_poke_types(poke: dict):
        if len(poke['types']) > 1:
            return [poke['types'][:]['type']['name']]
        return [poke['types'][0]['type']['name']]
