from flask import Flask, Response, redirect, request, session, abort, render_template, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import os
import sys
import json

sys.path.append(os.path.abspath(__file__) + "/../")
from database import *
config = json.load(open("config.json"))

db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

app = Flask(__name__)
app.config.update(dict(
    THREADS_PER_PAGE = 8,
    CSRF_ENABLED = True,
    CSRF_SESSION_KEY = "secret",
    SECRET_KEY = "secret",
))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from .controllers import *