class Config:
    APP_NAME = 'Quiz Master'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizmasterapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    URL = 'http://127.0.0.1:5000'
    MINIMUM_QUIZ_DURATION = 10
    MAXIMUM_QUIZ_DURATION = 200