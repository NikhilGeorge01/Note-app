from flask import Flask, render_template, url_for, views
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
lm = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "noter.db")
app.config['SECRET_KEY'] = 'this-is-my-secret'
db = SQLAlchemy(app)
lm.init_app(app)
lm.session_protection = "strong"
lm.login_view = "login"

# Import views and models after all initializations
from .views import *
