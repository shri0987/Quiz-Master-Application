from datetime import datetime
from repository.database import db

class Question(db.Model):
    __tablename__ = 'questions'
    questionId = db.Column(db.String(100), primary_key=True, nullable=False)
    quizId = db.Column(db.String(100), db.ForeignKey('quizzes.quizId', ondelete='CASCADE'), nullable=False)
    questionStatement = db.Column(db.String(1000), nullable=False)
    option1 = db.Column(db.String(500), nullable=False)
    option2 = db.Column(db.String(500), nullable=False)
    option3 = db.Column(db.String(500), nullable=False)
    option4 = db.Column(db.String(500), nullable=False)
    correctOption = db.Column(db.String(500), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    def __init__(self, questionId, quizId, questionStatement, option1, option2, option3, option4, correctOption, marks):
        self.questionId = questionId
        self.quizId = quizId
        self.questionStatement = questionStatement
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correctOption = correctOption
        self.marks = marks

    def to_dict(self):
        return {
            'questionId': self.questionId,
            'quizId': self.quizId,
            'questionStatement': self.questionStatement,
            'option1': self.option1,
            'option2': self.option2,
            'option3': self.option3,
            'option4': self.option4,
            'correctOption': self.correctOption,
            'marks': self.marks
        }
