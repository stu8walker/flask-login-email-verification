from app.main import bp
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Login"

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return "Dashboard"