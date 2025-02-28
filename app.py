import os
import logging
import secrets
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy

from models.admin import Admin
from models.user import User
from repository.database import db, migrate
from controllers.usercontroller import UserController
from controllers.admincontroller import AdminController

def create_app():
    app = Flask(__name__)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config.from_object(Config) 
    logging.basicConfig(filename = 'app.log', level = logging.INFO)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    CORS(app)
    UserController(app)
    AdminController(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
