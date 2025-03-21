from repository.database import db

class Chapter(db.Model):
    __tablename__ = 'chapters'
    chapterId = db.Column(db.String(100), primary_key=True, nullable=False)
    subjectId = db.Column(db.String(100), db.ForeignKey('subjects.subjectId', ondelete='CASCADE'), nullable=False)
    chapterName = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    createdOn = db.Column(db.DateTime)

    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete-orphan")

    def __init__(self, chapterId, subjectId, chapterName, description, createdOn):
        self.chapterId = chapterId
        self.subjectId = subjectId
        self.chapterName = chapterName
        self.description = description
        self.createdOn = createdOn

    def to_dict(self):
        return {
            'chapterId': self.chapterId,
            'subjectId': self.subjectId,
            'chapterName': self.chapterName,
            'description': self.description,
            'createdOn': self.createdOn
        }
