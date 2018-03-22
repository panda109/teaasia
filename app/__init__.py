# app/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_sse import sse
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'None'
login_manager.login_view = 'auth.login'
images = UploadSet('images', IMAGES)
csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app._static_folder = os.path.abspath("static/")
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .products import product as products_blueprint
    app.register_blueprint(products_blueprint, url_prefix='/product')
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .taiwan import taiwan as taiwan_blueprint
    app.register_blueprint(taiwan_blueprint, url_prefix='/taiwan')
    from .linebot import linebot as linebot_blueprint
    app.register_blueprint(linebot_blueprint, url_prefix='/linebot')
    from .notifysse import notifysse as notifysse_blueprint
    app.register_blueprint(notifysse_blueprint, url_prefix='/notifysse')
    app.register_blueprint(sse, url_prefix='/stream')
    return app
