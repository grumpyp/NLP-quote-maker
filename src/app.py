from flask import Flask
import config
import functions
from views import view

app = Flask(__name__)

# Routing
app.register_blueprint(view)

if __name__ == '__main__' and config.production == True:
    app.run()