from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'votre_cle_secrete'
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Configuration des dossiers statiques et uploads
    app.config['STATIC_FOLDER'] = os.path.join(basedir, 'static')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.config['STATIC_FOLDER'], 'uploads')
    
    # Création du dossier uploads s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Configuration SQLite
    db_path = os.path.join(os.path.dirname(basedir), 'db', 'gestion_stock.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    login_manager.login_view = 'routes.login'

    return app
