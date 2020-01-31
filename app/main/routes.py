from app.main import bp
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm, ResetPasswordRequestForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
import datetime
from app.email_token import generate_confirmation_token, confirm_token
from app.email import send_email
from app.decorators import check_confirmed
import sys # for printing to console


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
        
        """ Now handled through @check_confirm decorator on route
        if not user.email_confirmed:
            flash('Please verify your email address to access.', 'danger')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.unconfirmed')
            return redirect(next_page)
        elif not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
        """
         
    return render_template('main/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # Check if email address is already registered
        if not User.query.filter_by(email = form.email.data).first():
            user = User(first_name = form.first_name.data, surname = form.surname.data, 
                            email = form.email.data, password = hashed_password, 
                            registered_date=datetime.datetime.now(), email_confirmed=False)                   
            db.session.add(user)
            db.session.commit()
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('main.confirm_email', token=token, _external=True)
            html = render_template('main/registration_confirm_email.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            
            flash('Your new account has been created! Please check your email account to confirm your email address.', 'success')
            return redirect(url_for('main.login'))
        flash('Email address is already registered with an account.', 'danger')
        return redirect(url_for('main.register'))
    return render_template('main/register.html', form=form)

@bp.route('/confirm/<token>')
# @login_required
def confirm_email(token):
    try:
        print('token : ' + token, file=sys.stdout )
        email = confirm_token(token)
        print('email : ' + email, file=sys.stdout)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        user.email_confirmed_date = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.login'))

@bp.route('/dashboard', methods=['GET'])
@login_required
@check_confirmed
def dashboard():
    return render_template('main/dashboard.html', user=current_user.first_name)

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_password_token()
            print('token: ' + token)
            flash('If we have an account for the email provided, we will email you a reset link.', 'success')
            return redirect(url_for('main.login'))
        flash('If we have an account for the email provided, we will email you a reset link.', 'success')
    return render_template('main/reset_password_request.html', form=form)     

@bp.route('/unconfirmed')
@login_required
def unconfirmed(): 
    if current_user.email_confirmed:
        return redirect('main.dashboard')
    #flash('Please confirm your email address.', 'warning')
    return render_template('main/unconfirmed.html', user=current_user.first_name)