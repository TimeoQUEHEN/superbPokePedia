#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import os
import sqlite3 as sql
from os.path import exists


class ManageDB:
    def __init__(self, home_schema: str):
        """
        Initialise un tableau de données en lisant les fichiers situé dans le Dossier Data
        Deux Variables Connection et Cursor visant à accueillir les objets de même nom du module Sqlite3
        """
        self.schemas = []
        self.tables = {}
        self.current_schema = None
        self.connection = None
        self.cursor = None
        if not exists(home_schema):
            os.mkdir(home_schema)
        self.home_schema = home_schema

    def create_schema(self, schema: str):
        """
        Prends en paramètre un nom de schema et vérifie s'il existe
        Enregistre ça création dans la liste des schemas, et en cle dans
        le dictionnaire tables et lui attribut une liste en valeur
        :param schema:
        :return:
        """
        assert schema not in self.schemas, "Le Schema existe déjà"
        self.connection = sql.connect(schema + ".db")
        self.schemas.append(schema)
        self.tables[schema] = []

    # Manage Methods
    def connexion(self, schema: str) -> bool:
        """
        Appel la méthode close_all pour établir une connexion
        sécurisé et ne pas perdre les données précédemment saisies

        Enfin, vérifie si la table demandée existe, et établie
        la connexion ainsi qu'un curseur sur celle-ci

        Retourne le Bon ou mauvais déroulement de la fonction avec un booléen
        :param schema:
        :return bool:
        """
        self.safe_close()
        if schema in self.schemas:
            self.connection = sql.connect(f"./Data/{schema}.db")
            self.cursor = self.connection.cursor()
            for table in self.cursor.execute("select name from sqlite_master where type='table';").fetchall():
                self.tables[schema].append(table[0])
            print(f"Connexion Établie avec la Base de donnée {schema}")
            return True
        else:
            print("La base de données n'existe pas")
            return False

    def check_connection(self) -> bool:
        """
        Vérifie si une connexion est actuellement ouverte et retourne directement le résultat du test
        :return bool:
        """
        return self.cursor is not None and self.connection is not None

    def save(self) -> bool:
        """
        Vérifie la connexion
        Sauvegarde les modifications réalisées dans la base de données actuellement connectée
        :return bool:
        """
        if self.check_connection():
            self.connection.commit()
            print("Modification(s) Sauvegardée(s)")
            return True
        else:
            print("Nothing to Save")
            return False

    def safe_close(self):
        """
        Réaliser une confirmation de management
        Ferme la base de données de manière sécurisée
        Sauvegarde les modifications effectuées
        :return:
        """
        if self.check_connection():
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Connexion End")
        else:
            print("Nothing to close")

    def force_close(self):
        """
        Vérifie tout de même si une connexion est ouverte
        pour éviter toute erreur et ferme la connexion sans
        sauvegarder les changements
        :return:
        """
        if self.check_connection():
            self.cursor.close()
            self.connection.close()
        else:
            print("Nothing to Close")
            return False

    def show_tables(self, schema) -> list:
        """
        Retourne une liste de tables d'un schéma particulier
        fourni en paramètre
        :param schema:
        :return list:
        """
        return self.tables[schema]

    # Manipulation Methods
    def create_table(self, args: str) -> bool:
        """
        Réalise une vérification sur la commande sur les deux premiers mots
        Et execute la commande en vérifiant la connexion sans vérification supplémentaire
        :param args:
        :return bool:
        """
        assert args[:6] == "create" and args[7:12] == "table", "Command must be CREATE TABLE"
        if self.check_connection():
            self.cursor.execute(args)
            self.tables[self.current_schema].append((args.split(" ")[3]))
            return True
        else:
            print("Veuillez établir une connexion sur un Fichier de base base de donnée")
            return False

    def delete_table(self, args):
        """
        Réalise une vérification de commande sur le premier mot
        Puis vérifie si la table existe
        Et execute la suppression de la table
        :param args:
        :return:
        """
        assert args[0:4] == "" and args[5:10] == "", "Command must be DROP TABLE"
        if args.split(" ")[3] in self.tables:
            self.cursor.execute(args)
            self.tables[self.current_schema].remove(args.split(" ")[3])

    def insertion(self, args):
        """
        Réalise une verification de commande sur les premiers mots
        Et execute l'ajout de données sans vérification supplémentaire
        :param args:
        :return:
        """
        assert args[0:6] == "insert" and args[7:11] == "into", "Command must be INSERT INTO"
        self.cursor.execute(args)

    def delete_data(self, args: str):
        """
        Réalise une verification de commande sur les premiers mots
        Et execute la suppression de données sans vérification supplémentaire
        :param args:
        :return:
        """
        assert args[0:6] == "delete" and args[7:11] == "from", "Command must be DELETE FROM"
        self.cursor.execute(args)

    def selection(self, args) -> list:
        """
        Réalise une vérification de commande sur le premier mot
        Et Affiche tous les résultats de la sélection
        :param args:
        :return data <list[tuple]>:
        """
        assert args[0:6] == "select", "Command must be SELECT"
        data = self.cursor.execute(args).fetchall()
        return data
