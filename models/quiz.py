from repository.database import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quizId = db.Column(db.String(100), primary_key=True, nullable=False)
    chapterId = db.Column(db.String(100), db.ForeignKey('chapters.chapterId', ondelete='CASCADE'), nullable=False)
    quizDate = db.Column(db.DateTime, nullable=False)
    timeDurationMinutes = db.Column(db.Integer, nullable = False)
    remarks = db.Column(db.String(100), nullable=True)

    def __init__(self, quizId, chapterId, quizDate, timeDurationMinutes, remarks):
        self.quizId = quizId
        self.chapterId = chapterId
        self.quizDate = quizDate
        self.timeDurationMinutes = timeDurationMinutes
        self.remarks = remarks

    def to_dict(self):
        return {
            'quizId': self.quizId,
            'chapterId': self.chapterId,
            'quizDate': self.quizDate,
            'timeDurationMinutes': self.timeDurationMinutes,
            'remarks' : self.remarks
        }
