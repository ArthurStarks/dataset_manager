from flask import Blueprint, render_template

home_bp = Blueprint('datasetmanager', __name__)

@home_bp.route('/')
def datasetmanager():
    return render_template('auth/login.html')  
