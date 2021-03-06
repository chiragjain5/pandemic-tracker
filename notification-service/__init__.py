from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

"""Construct the core application."""
app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)