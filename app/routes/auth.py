from flask import Blueprint, app, render_template, redirect, session, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
           session.clear()
           login_user(user)
           session.modified = True

           if (user.role == "data-scientist") :
             return redirect(url_for('data.dashboard'))  # Redirect to home or a dashboard
           else : 
               return redirect(url_for('admin.dashboard')) 
        flash('Invalid username or password', 'danger')
    return render_template('login.html')



@auth_bp.route('/register', methods=['GET', 'POST'])

def register():
   if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
      
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        
      
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('username already registered', 'warning')
            return redirect(url_for('auth.register'))
        
     
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        
        try:
            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account.', 'danger')
            print(f"Error: {e}")  # For debugging
            return redirect(url_for('auth.register'))
    
    
   return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect("auth.login") 