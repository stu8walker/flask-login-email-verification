import os, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
#login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init modules and packages
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # Import blueprint from routes.py
    from app.main import bp
    app.register_blueprint(bp)
    
    # Example of testing to see if running in dev environment
    #if app.env == 'development':
    #    app.logger.info('Development Environment!') 
    
    # Further configure app. settings here
    
    return app


# Import goes after app creation to avoid circular imports
from app import models