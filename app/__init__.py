import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import User

from .extensions import db
from .extensions import login_manager
from .extensions import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.data import data_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(data_bp, url_prefix='/data')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set the login view for redirecting unauthorized users
    login_manager.login_view = 'auth.login'

       
    @app.route('/')
    def home():
     return redirect(url_for('auth.login'))

    return app
