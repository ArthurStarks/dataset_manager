from flask import Blueprint, render_template
from flask_login import login_required
from ..models import User, Dataset
from ..utils import role_required

admin_bp= Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    users = User.query.all()
    datasets = Dataset.query.all()
    return render_template('admin_dashboard.html', users=users, datasets=datasets)
