import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def affichage():
    return render_template("index.html")

@app.route("/<pokemon>", methods=["GET"])
def pokemon(pokemon = None):
    return render_template("pokemon.html", pokemon = pokemon)

@app.route("/account", methods=["POST"])
def exo1():
    return render_template("account.html")