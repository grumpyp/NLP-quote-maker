from flask import Flask
from .views import view
from .config import log_file, production

import src.functions 

import logging

logging.basicConfig(
    filename=log_file,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


app = Flask(__name__)

app.register_blueprint(view)

if __name__ == '__main__' and production == True:
    logger.debug("Going to start app ")
    app.run()
