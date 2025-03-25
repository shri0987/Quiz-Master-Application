from datetime import timedelta
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
from models.subject import Subject
from models.chapter import Chapter
from models.question import Question
from models.quiz import Quiz
from models.score import Score
from models.response import Response
from repository.database import db, migrate
from apicontrollers.userapicontroller import UserController
from apicontrollers.adminapicontroller import AdminController
from apicontrollers.subjectapicontroller import SubjectController
from apicontrollers.chapterapicontroller import ChapterController
from apicontrollers.quizapicontroller import QuizController
from apicontrollers.questionapicontroller import QuestionController

def create_app():
    app = Flask(__name__)
    secret_key = 'b7a8f6d3c9e12f4a5b6c7d8e9f0a1b2c'
    app.secret_key = secret_key
    app.permanent_session_lifetime = timedelta(hours=1)
    app.config.from_object(Config) 
    logging.basicConfig(filename = 'app.log', level = logging.INFO)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    CORS(app)
    UserController(app)
    AdminController(app)
    SubjectController(app)
    ChapterController(app)
    QuizController(app)
    QuestionController(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
 