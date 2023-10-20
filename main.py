import requests as requests
from flask import Flask, render_template, redirect
from markupsafe import escape
from datetime import datetime, date

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = "Welcome to SPP"


@app.route("/")
def index():
    return render_template('index.html',var="sexe")

@app.route("/poke")
def pokemon():
    return render_template('pokemon.html',pokemon_name="sexe",pok_name_fr="bite",pok_name_eng="dick",sprite="sprite",sprite_shiny="SS",sprite_region_diff="diff",stats_du_pok=["150","300"])
