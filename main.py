from flask import Flask, render_template, request, redirect

# python -m flask --app .\nom_du_fichier\ run

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route("/")
@app.route("/<pokemon>", methods=["GET"])
def pokemon(pokemon=None):
    if pokemon is None:
        return render_template("index.html")
    return render_template("pokemon.html", pokemon=pokemon)


@app.route("/account", methods=["GET"])
def account():
    # Récupérer l'utilisateur grace au cookie
    return render_template("account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # Récupérer l'utilisateur dans la base de donnée (peut être vérifier s'il n'y pas d'erreur)
        return redirect("/account")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Créer l'utilisateur dans la base de donnée (peut être vérifier s'il n'y pas d'erreur)
        return redirect("/account")


if __name__ == "__main__":
    app.run()
