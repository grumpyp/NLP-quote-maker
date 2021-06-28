from flask import render_template
from flask import Blueprint
from flask import request, Response
from .src import functions
from .src import db

from bson.json_util import dumps
import logging

view = Blueprint("view", __name__)

logger = logging.getLogger(__name__)

@view.route('/')
def index():
    return  render_template('index.html')


@view.get('/quotes')
def get_quotes():

    quote = request.args.get('quote')
    data = db.fetch_quotes_by_ratings(quote)
    logger.debug(f'Found matching quotes count  {len(data)}')
    
    return render_template('index.html', data = data)