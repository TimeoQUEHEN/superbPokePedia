from flask import Flask, render_template

# python -m flask --app .\nom_du_fichier\ run

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route("/")
def affichage():
    return render_template("index.html")


@app.route("/<pokemon>", methods=["GET"])
def pokemon(poke=None):
    return render_template("pokemon.html", pokemon=poke)


@app.route("/account", methods=["POST"])
def exo1():
    return render_template("account.html")


if __name__ == "__main__":
    app.run()