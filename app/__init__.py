from flask import Flask
from views import view
import config

from src.functions import sentiment_rating

import src.db as db

import logging

logging.basicConfig(
    filename=config.log_file,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


app = Flask(__name__)

app.register_blueprint(view)

if __name__ == '__main__' and config.production == True:
    logger.debug("Going to start app ")
    logger.debug(f'"DB connection test ", {db.test_db()}')
    app.run()
