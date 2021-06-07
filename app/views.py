from flask import render_template, Blueprint
from app.src import functions
from app.src import db


view = Blueprint("view", __name__)

@view.get('/')
def hello():
    return 'Hello World!'
