from app import create_app, db
from app.models import User 
from werkzeug.security import generate_password_hash

def seed_admin():
    app = create_app()
    with app.app_context():
      
        if User.query.filter_by(username="admin").first():
            print("Admin user already exists.")
            return

    
        admin_user = User(
            username="admin",
            password=generate_password_hash("adminpassword", method="pbkdf2:sha256")
        )

        # Add and commit the user to the database
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")

if __name__ == "__main__":
    seed_admin()
