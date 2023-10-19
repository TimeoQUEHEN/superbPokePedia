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
