from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy

from .api_routes import api_route
from .auth_routes import auth_route
from ..models.db_models import db
from ..config import config

flask_app = Flask(__name__)
flask_app.register_blueprint(api_route)
flask_app.register_blueprint(auth_route)

conf = config.load_config()

db_conf = conf.database
flask_app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{db_conf.dbuname}:{db_conf.dbpass}@{db_conf.dburl}/{db_conf.dbname}"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(flask_app)

with flask_app.app_context():
    db.create_all()


flask_app.config["UPLOAD_CONFIG"] = conf.upload

flask_app.config["JWT_SECRET_KEY"] = "8b01591330f944b08fc2a03ab48a85aa"
