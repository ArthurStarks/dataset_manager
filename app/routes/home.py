from flask import Blueprint, render_template

home_bp = Blueprint('datasetmanager', __name__)

@home_bp.route('/datasetmanager')
def datasetmanager():
    return render_template('auth/login.html')  # Create home.html in the templates folder
