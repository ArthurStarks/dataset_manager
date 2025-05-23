import csv
import os
import pandas as pd
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


@data_bp.route('/delete/<int:dataset_id>', methods=['POST'])
@login_required
def delete_dataset(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id, user_id=current_user.id).first()

    if dataset:
        db.session.delete(dataset)
        db.session.commit()
        flash("Dataset deleted successfully!", "success")
    else:
        flash("Dataset not found or you don't have permission to delete it.", "danger")

    return redirect(url_for('data.dashboard'))

@data_bp.route('/dataset/<int:dataset_id>')
@login_required
def view_dataset(dataset_id):
    file = Dataset.query.get_or_404(dataset_id)
    file_extension = os.path.splitext(file.path)[1].lower()  # Get the file extension
    csv_content = []

    try:
        if file_extension == '.csv':
            # Read CSV file
            with open(file.path, newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                for row in csv_reader:
                    csv_content.append(row)
        elif file_extension in ['.xls', '.xlsx']:
            # Read Excel file using pandas
            df = pd.read_excel(file.path)
            csv_content = df.values.tolist()  
            csv_content.insert(0, df.columns.tolist())  
        else:
            return "Unsupported file type", 400
    except Exception as e:
        return f"Error reading file: {e}", 500

    return render_template('data/read_file.html', csv_content=csv_content)

@data_bp.route('/dataset_info/<int:dataset_id>')
@login_required
def dataset_info(dataset_id):
    file = Dataset.query.get_or_404(dataset_id)
   
    file_path = os.path.join('uploads', f'{file.name}')

    try:
        # Determine file extension and load dataset accordingly
        if file.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            flash('Unsupported file format. Only CSV and XLSX are supported.', 'danger')
            return redirect(url_for('data.dashboard'))
        
        # Collect general info
        num_rows = df.shape[0]
        num_columns = df.shape[1]
        column_names = df.columns.tolist()
        null_values = df.isnull().sum().to_dict()
        data_types = df.dtypes.to_dict()

        dataset_summary = {
            'num_rows': num_rows,
            'num_columns': num_columns,
            'column_names': column_names,
            'null_values': null_values,
            'data_types': data_types
        }

        return render_template('data/dataset_info.html', dataset_summary=dataset_summary, user=current_user)

    except FileNotFoundError:
        flash('File not found.', 'danger')
        return redirect(url_for('data.dashboard'))
    except Exception as e:
        flash(f'Error reading dataset: {str(e)}', 'danger')
        return redirect(url_for('data.dashboard'))
    
