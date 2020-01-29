from app import db, login
from flask_login import UserMixin


# Example model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registered_date = db.Column(db.DateTime, nullable=False) # need default?
    email_confirmed = db.Column(db.Boolean, nullable=False)
    email_confirmed_date = db.Column(db.DateTime, nullable=True)
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))