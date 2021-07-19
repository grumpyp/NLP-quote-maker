from flask import Flask
import .views
import .config

import src.functions 

import logging

logging.basicConfig(
    filename=config.log_file,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


app = Flask(__name__)

app.register_blueprint(views.view)

if __name__ == '__main__' and config.production == True:
    logger.debug("Going to start app ")
    app.run()
