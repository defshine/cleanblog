from flask import Flask
from models import db
from views import bp
from app.admin import create_admin
from flask.ext.login import LoginManager
from app.filters import babel, my_format_datetime, format_meta_keywords


def create_app():

    app = Flask(__name__)
    app.config.from_object('config')

    register_babel(app)
    register_jinjia_filters(app)
    init_login(app)
    register_blueprints(app)
    register_database(app)
    create_admin(app)

    return app


def register_blueprints(app):
    app.register_blueprint(bp)


def register_database(app):
    db.init_app(app)


def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.objects(id=user_id).first()


def register_babel(app):
    babel.init_app(app)


def register_jinjia_filters(app):
    app.jinja_env.filters['my_format_datetime'] = my_format_datetime
    app.jinja_env.filters['format_meta_keywords'] = format_meta_keywords
