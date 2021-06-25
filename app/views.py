from re import search
from flask import render_template, jsonify, request
from flask import Blueprint
from flask import Response
from .src import functions
from .src import db


from bson.json_util import dumps

view = Blueprint("view", __name__)

@view.get('/')
def hello():
    return render_template("index.html")

@view.route('/livesearch', methods=["POST"])
def livesearch():
    searchbox = request.form.get("text")
    print(searchbox)
    rating = functions.Rating()
    searchbox_rating = rating.sentiment_rating(searchbox)
    result = str(searchbox_rating)    #convert json to str to try 
    return result


@view.get('/quotes')
def get_quotes():
    return Response(response=dumps(db.fetch_all_quotes()))
