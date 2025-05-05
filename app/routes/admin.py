from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from ..models import User, Dataset
from ..utils import role_required
from app import db

admin_bp= Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')

def dashboard():
    users = User.query.all()
    return render_template('index.html', users=users)


@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Dataset deleted successfully!", "success")
    else:
        flash("Dataset not found or you don't have permission to delete it.", "danger")

    return redirect(url_for('admin.dashboard'))
