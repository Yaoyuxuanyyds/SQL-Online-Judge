from app import create_app
from exts import db
from models import Admin

def create_admin():
    app = create_app()
    with app.app_context():
        new_admin = Admin(id='admin1', name='admin', password='123456')
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully")

if __name__ == "__main__":
    create_admin()
