"""Determines app routing and configures database"""
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from spacetrader import routes
#from enum import Enum

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaf2e614c424b1cdb71d9e4678dd3b1bfd60369331569029'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from spacetrader import routes
