from flask import render_template, Blueprint
import functions


view = Blueprint("view", __name__)

@view.route('/', methods=["GET"])
def hello():
    return 'Hello World!'