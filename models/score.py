from repository.database import db

class Score(db.Model):
    __tablename__ = 'scores'
    scoreId = db.Column(db.String(100), primary_key=True, nullable=False)
    quizId = db.Column(db.String(100), db.ForeignKey('quizzes.quizId', ondelete='CASCADE'), nullable=False)
    userId = db.Column(db.String(100), db.ForeignKey('users.userId', ondelete='CASCADE'), nullable=False)
    attemptTime = db.Column(db.DateTime, nullable = False)
    totalScored = db.Column(db.Integer, nullable=False)

    def __init__(self, scoreId, quizId, userId, totalScored):
        self.scoreId = scoreId
        self.quizId = quizId
        self.userId = userId
        self.totalScored = totalScored

    def to_dict(self):
        return {
            'scoreId': self.scoreId,
            'quizId': self.quizId,
            'userId': self.userId,
            'attemptTime': self.attemptTime,
            'totalScored': self.totalScored
        }
