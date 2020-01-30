from app.main import bp
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
import datetime


@bp.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Your email or password is incorrect. Please try again', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        
        # Should check if the url is safe for redirects
        # Any argument not for site should be redirected
        # e.g. 127.0.0.1:5000/login?next=http://some-malicious-site.com
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('main/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # Check if email address is already registered
        if not User.query.filter_by(email = form.email.data).first():
            new_user = User(first_name = form.first_name.data, surname = form.surname.data, 
                            email = form.email.data, password = hashed_password, 
                            registered_date=datetime.datetime.now(), email_confirmed=False)                   
            db.session.add(new_user)
            db.session.commit()
            flash('Your new account has been created! Time to login.', 'success')
            return redirect(url_for('main.login'))
        flash('Email address is already registered with an account.', 'danger')
        return redirect(url_for('main.register'))
    return render_template('main/register.html', form=form)

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user.first_name)

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))