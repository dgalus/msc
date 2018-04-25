from flask import Flask, Response, redirect, request, session, abort, render_template, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import os

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    DATABASE_CONNECT_OPTIONS = {},
    THREADS_PER_PAGE = 8,
    CSRF_ENABLED = True,
    CSRF_SESSION_KEY = "secret",
    SECRET_KEY = "secret",
))

db = SQLAlchemy(app)

from .models import *

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from .controllers import *