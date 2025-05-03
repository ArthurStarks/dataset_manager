from flask import Blueprint, render_template, request
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

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Perform basic EDA
            df = pd.read_csv(filepath)
            num_rows, num_cols = df.shape

            # Save to database
            dataset = Dataset(
                name=filename,
                file_path=filepath,
                num_rows=num_rows,
                num_cols=num_cols,
                upload_date=datetime.now()
            )
            db.session.add(dataset)
            db.session.commit()

            flash('Dataset uploaded successfully!', 'success')
            return redirect(url_for('view_datasets'))
        else:
            flash('Invalid file type. Please upload a CSV file.', 'danger')
    return render_template('upload.html')
