from flask import render_template, Blueprint
from src import functions
from src import db


view = Blueprint("view", __name__)

@view.get('/')
def hello():
    return 'Hello World!'
