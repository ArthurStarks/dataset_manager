from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Dataset
from ..utils import role_required

data_bp = Blueprint('data', __name__)

@data_bp.route('/dashboard')

@login_required
@role_required('data-scientist')
def dashboard():

    datasets = Dataset.query.filter_by(user_id=current_user.id).all()
    return render_template('data/index.html', datasets=datasets, user=current_user)



@data_bp.route('/upload')

@login_required
@role_required('data-scientist')
def upload():

    datasets = Dataset.query.filter_by(user_id=current_user.id).all()
    return render_template('data/index.html', datasets=datasets, user=current_user)
