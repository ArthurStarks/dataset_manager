from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))  # Redirect to home or a dashboard
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html')



@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Registration logic here
    pass

@auth_bp.route('/logout')
@login_required
def logout():
    # Logout logic here
    pass
