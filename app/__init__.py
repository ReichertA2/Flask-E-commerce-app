from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#init plug-ins 
login = LoginManager()

#init my Database Manager
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    #init the app 
    app=Flask(__name__)
    #link in the config
    app.config.from_object(config_class)

    #register plug-ins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    #configure some settings
    login.login_view='auth.login'
    login.login_message = 'Please log in'
    login.login_message_category = 'warning'

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app