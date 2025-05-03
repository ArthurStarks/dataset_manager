from flask import Blueprint

# Importing the individual routes
from .auth import auth_bp
from .admin import admin_bp
from .data import data_bp
from .home import home_bp

def register_routes(app):
    # Registering blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # All auth routes will have /auth prefix
    app.register_blueprint(admin_bp, url_prefix='/admin')  # All admin routes will have /admin prefix
    app.register_blueprint(data_bp, url_prefix='/data')  # All data-scientist routes will have /data prefix
    app.register_blueprint(home_bp, url_prefix="/datasetmanager")

