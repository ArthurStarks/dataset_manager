from functools import wraps
from app import  db
from flask import app, current_app, request, redirect, url_for, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app.models import User

def role_required(role):
    """
    Decorator to restrict access to users with specific roles.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You need to log in to access this page.", "warning")
                return redirect(url_for('auth.login'))
            if current_user.role != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("auth.login"))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

