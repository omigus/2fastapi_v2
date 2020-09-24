from flask import Flask
from flask_bcrypt import Bcrypt
from .config import config_by_name
from flask_cors import CORS
# db = SQLAlchemy()
# ma = Marshmallow()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_by_name[config_name])
    # db.init_app(app)
    # ma.init_app(app)
    flask_bcrypt.init_app(app)

    return app