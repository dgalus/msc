from flask import Flask, Response, redirect, request, session, abort, render_template, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import os
import sys

sys.path.append(os.path.abspath(__file__) + "/../")
from database import *
db = Database("sniffer", "sniffer", "127.0.0.1", 5432, "sniffer")

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