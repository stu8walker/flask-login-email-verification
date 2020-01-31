from app import db, login
from flask import current_app
from flask_login import UserMixin
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
            
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    