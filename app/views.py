from flask import render_template
from flask import Blueprint
from flask import Response
from .src import functions
from .src import db

from bson.json_util import dumps

view = Blueprint("view", __name__)

@view.get('/')
def hello():
    return 'Hello World!'


@view.get('/quotes')
def get_quotes():
    return Response(response=dumps(db.fetch_all_quotes()))
