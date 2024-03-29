
from flask import Flask, render_template, request, redirect, make_response

from app.module.Manage_DataBase import ManageDB
from app.Pokemon import *

# python -m flask --app main run

database = ManageDB("database.sqlite")
api = PokeInteract()


def init_database():
    try:
        database.create_schema("user")
        database.connexion("user")
        database.create_table("CREATE TABLE user(user_id INTEGER PRIMARY KEY, user_name TEXT NOT NULL, user_email "
                              "TEXT UNIQUE NOT NULL, user_password TEXT NOT NULL);")
        database.create_table("CREATE TABLE favorite(user_id INTEGER REFERENCES user(user_id), pokemon TEXT NOT NULL, "
                              "PRIMARY KEY(user_id, pokemon));")
        database.force_close()
    except:
        database.force_close()


init_database()

def get_user(id):
    if id is None:
        return {'connecte': False}
    database.connexion("user")
    user = database.cursor.execute("SELECT * FROM user WHERE user_id = ?;", [id]).fetchone()
    database.force_close()
    return {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3], 'connecte': True}

def cryptage(password):
    return password

def verification_email(email):
    email1 = email.split(' ')
    email2 = email1[0].split('@')
    return len(email1) == 1 and len(email2) == 2 and len(email2[1].split('.')) == 2


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route("/")
def acceuil():
    try:
        user = get_user(request.cookies.get("user_id"))
        favorites = []
        database.connexion("user")
        for pokemon in database.cursor.execute("SELECT pokemon FROM favorite WHERE user_id = ?;", [request.cookies.get("user_id")]).fetchall():
            favorites.append(Pokemon(pokemon[0]))
        database.force_close()
        return render_template("index.html", user=user, favorites=favorites)
    except:
        return redirect('/logout')


@app.route("/search", methods=["POST"])
def search():
    return redirect("/"+request.form["pokemon"])


@app.route("/<pokemon>", methods=["GET"])
def pokemon(pokemon='pikachu'):
    user = get_user(request.cookies.get("user_id"))
    poke = Pokemon(pokemon)
    database.connexion("user")
    favorite = database.cursor.execute("SELECT * FROM favorite WHERE user_id = ? AND pokemon = ?;", [request.cookies.get("user_id"), pokemon]).fetchone() is not None
    database.force_close()
    return render_template("pokemon.html", user=user, pokemon=poke, favorite=favorite)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if request.cookies.get("user_id") is not None:
            return redirect('/')
        return render_template("login.html", user={"connecte": False})
    else:
        try:
            database.connexion("user")
            user = (request.form["email"], cryptage(request.form["password"]))
            id = database.cursor.execute("SELECT user_id FROM user WHERE user_email = ? AND user_password = ?;",
                                         user).fetchone()[0]
            database.force_close()
            assert id is not None, "Email ou Mot de passe incorrect"
            vue = redirect('/')
            vue.set_cookie('user_id', str(id))
            return vue
        except:
            database.force_close()
            return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if request.cookies.get("user_id") is not None:
            return redirect('/')
        return render_template("register.html", user={"connecte": False})
    else:
            try:
                database.connexion("user")
                new_id = database.selection("SELECT MAX(user_id) FROM user;")[0][0]
                if new_id is None:
                    new_id = -1
                user = (new_id + 1, request.form["name"], request.form["email"], cryptage(request.form["password"]))
                assert (user[1] is not None and user[2] is not None and user[3] is not None and verification_email(user[2])
                        and user[3] == cryptage(request.form["confirmation_password"])), "Informations incorrectes"
                database.cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?);", user)
                database.save()
                database.force_close()
                vue = redirect('/')
                vue.set_cookie('user_id', str(user[0]))
                return vue
            except:
                database.force_close()
                return redirect("/register")


@app.route('/logout', methods=["GET"])
def logout():
    vue = redirect('/')
    vue.delete_cookie('user_id')
    return vue


@app.route('/<pokemon>/favorite', methods=["POST"])
def favorite(pokemon='pikachu'):
    if request.cookies.get("user_id") is None:
        return redirect("/login")
    try:
        database.connexion("user")
        favorite = [request.cookies.get("user_id"), pokemon]
        if database.cursor.execute("SELECT * FROM favorite WHERE user_id = ? AND pokemon = ?;", favorite).fetchone() is None:
            database.cursor.execute("INSERT INTO favorite VALUES (?, ?);", favorite)
        else:
            database.cursor.execute("DELETE FROM favorite WHERE user_id = ? AND pokemon = ?;", favorite)
        database.save()
        database.force_close()
        return redirect('/'+pokemon)
    except:
        database.force_close()
        return redirect('/')


if __name__ == "__main__":
    app.run()
