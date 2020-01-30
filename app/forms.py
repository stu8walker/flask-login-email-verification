from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired


class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="Please enter your first name"), 
        Length(min=4, max=20)])
    surname = StringField('Surname', validators=[InputRequired(message="Please enter your surname"), 
        Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(message="Please enter your email address"), 
        Email(message="Please provide a valid email address"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter a password"), 
        Length(min=8, max=80)])
    password2 = PasswordField('Repeat Password', 
        validators=[InputRequired(message="Please repeat your password"), 
        EqualTo('password', message="The passwords you entered do not match. Please try again."), 
        Length(min=8, max=80)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Please enter your email address"), 
        Email(message='Please provide a valid email address')])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your password")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')