import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..models import Dataset
from ..utils import allowed_file, role_required
from app import db
from werkzeug.utils import secure_filename


data_bp = Blueprint('data', __name__)

@data_bp.route('/dashboard')

@login_required
@role_required('data-scientist')
def dashboard():

    datasets = Dataset.query.filter_by(user_id=current_user.id).all()
    return render_template('data/index.html', datasets=datasets, user=current_user)



@data_bp.route('/upload', methods=['GET', 'POST'])

@login_required
@role_required('data-scientist')
def upload():

   if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # type: ignore
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Save to database
            dataset = Dataset(name=filename, path=save_path, user_id=current_user.id)
            db.session.add(dataset)
            db.session.commit()

            flash('File successfully uploaded', 'success')
            return redirect(url_for('data.upload'))

        flash('Invalid file type', 'danger')

   return render_template('data/upload.html',user=current_user)