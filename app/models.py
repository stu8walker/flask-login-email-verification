from app import db, login
from flask import current_app, redirect, flash
from flask_login import UserMixin
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import sys

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
        self.password = generate_password_hash(password, method='sha256')
    
    def generate_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except jwt.ExpiredSignatureError:
            # Signature has expired
            print("Token has expired!", file=sys.stdout)
            return
        except:    
            return
        return User.query.get(id)
    
    def generate_email_verification_token(self, expires_in=600):
        return jwt.encode(
            {'verify_email': self.email, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_email_verification_token(token):
        try:
            email = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['verify_email']
        except jwt.ExpiredSignatureError:
            # Signature has expired
            print("Token has expired!", file=sys.stdout)
            return
        except:
            return
        return User.query.filter_by(email = email).first()
    
            
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    