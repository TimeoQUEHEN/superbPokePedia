#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import requests


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
