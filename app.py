from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hello123'

from models import db, User

db.init_app(app)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(is_admin=True).first()

    if not admin:
        admin = User(
            username='admin',
            passhash=generate_password_hash('admin123'),
            name='Admin',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

import routes

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)