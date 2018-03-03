from flask import Flask, Response, redirect, request, session, abort, render_template, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .models import *

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from .controllers import *