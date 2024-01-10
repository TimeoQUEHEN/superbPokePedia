import bcrypt
from flask import Flask, render_template, request, redirect, make_response

from app.module.Manage_DataBase import ManageDB

# python -m flask --app .\nom_du_fichier\ run

database = ManageDB("database.sqlite")


def init_database():
    try:
        database.create_schema("user")
        database.connexion("user")
        database.create_table("CREATE TABLE user(user_id INTEGER PRIMARY KEY, user_name TEXT NOT NULL, user_email "
                              "UNIQUE TEXT NOT NULL, user_password TEXT NOT NULL);")
        database.create_table("CREATE TABLE favorite(user_id INTEGER REFERENCES user(user_id), pokemon TEXT NOT NULL, "
                              "PRIMARY KEY(user_id, pokemon));")
        database.create_table("CREATE TABLE sound(pokemon TEXT PRIMARY KEY, name_file TEXT);")
    except:
        database.force_close()


init_database()


def cryptage(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route("/")
def acceuil():
    return render_template("index.html")


@app.route("/pokemon/<pokemon>", methods=["GET"])
def pokemon(pokemon=None):
    return render_template("pokemon.html", pokemon=pokemon)


@app.route("/account", methods=["GET"])
def account():
    try:
        database.connexion("user")
        user = (database.cursor.execute("SELECT * FROM user WHERE user_id = ?;", [request.cookies.get("user_id")])
                .fetchone())
        database.force_close()
        return render_template("account.html", user=user)
    except:
        database.force_close()
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        try:
            database.connexion("user")
            id = database.cursor.execute("SELECT id FROM user WHERE user_email = ? AND user_password = ?;",
                                         [request.form["user_email"],
                                          cryptage(request.form["user_password"])]).fetchone()
            database.force_close()
            assert id is not None, "Email ou Mot de passe incorrect"
            vue = resp = make_response(render_template('account.html'))
            resp.set_cookie('user_id', id)
            return vue
        except:
            database.force_close()
            return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        try:
            database.connexion("user")
            new_id = database.selection("SELECT MAX(id) FROM user;")[0] + 1
            database.cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?);", [new_id, request.form["user_name"],
                                                                              request.form["user_email"],
                                                                              cryptage(request.form["user_password"])])
            database.force_close()
            return redirect("/account")
        except:
            database.force_close()
            return redirect("/register")


if __name__ == "__main__":
    app.run()
