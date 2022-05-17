import os

from flask import Flask
from .models import db, User
from .auth import auth as auth_blueprint
from .stratigraphy import stratigraphy as stratigraphy_blueprint
from flask_jwt_extended import JWTManager


# Using factory app
def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        # SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
        SQLALCHEMY_DATABASE_URI="sqlite:///project.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
    )

    db.app = app
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)
    # blueprint for stratigraphy part of app
    app.register_blueprint(stratigraphy_blueprint)

    return app
