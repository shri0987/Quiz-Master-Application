from repository.database import db
from sqlalchemy.sql import func

class Response(db.Model):
    __tablename__ = 'responses'
    
    responseId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False) 
    quizId = db.Column(db.String(100), db.ForeignKey('quizzes.quizId', ondelete='CASCADE'), nullable=False)
    questionId = db.Column(db.String(100), db.ForeignKey('questions.questionId', ondelete='CASCADE'), nullable=False)
    userName = db.Column(db.String(100), db.ForeignKey('users.userName', ondelete='CASCADE'), nullable=False)
    userResponse = db.Column(db.String(255), nullable=False)
    marksScored = db.Column(db.Integer, nullable=False)
    attemptTime = db.Column(db.DateTime, nullable=False)
    isQuestionVisited = db.Column(db.Boolean, nullable = False)

    def __init__(self, quizId, questionId, userName, userResponse, marksScored, attemptTime, isQuestionVisited):
        self.quizId = quizId
        self.questionId = questionId
        self.userName = userName
        self.userResponse = userResponse
        self.marksScored = marksScored
        self.attemptTime = attemptTime
        self.isQuestionVisited = isQuestionVisited

    def to_dict(self):
        return {
            'quizId': self.quizId,
            'questionId': self.questionId,
            'userName': self.userName,
            'userResponse': self.userResponse,
            'marksScored': self.marksScored,
            'attemptTime': self.attemptTime,
            'isQuestionVisited': self.isQuestionVisited
        }
