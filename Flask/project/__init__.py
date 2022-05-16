from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


# Using factory app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '\x91\xdb]\xde\'" \xd7\xe2\x97\r[\xd5%\x0bI\'\x91_"\x81\x07\xe2Z'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    # user loader tells how to find specific user from the id that is stored
    # in their cookie session
    @login_manager.user_loader
    def load_user(user_id):
        # user id is the pk, it will be used in queries
        return User.query.get(int(user_id))


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
