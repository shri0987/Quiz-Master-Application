from repository.database import db

class Chapter(db.Model):
    __tablename__ = 'chapters'

    chapterId = db.Column(db.String, primary_key=True, nullable=False)
    subjectId = db.Column(db.String, db.ForeignKey('subjects.subjectId', ondelete='CASCADE'), nullable=False)
    chapterName = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

    def __init__(self, chapterId, subjectId, chapterName, description):
        self.chapterId = chapterId
        self.subjectId = subjectId
        self.chapterName = chapterName
        self.description = description

    def to_dict(self):
        return {
            'chapterId': self.chapterId,
            'subjectId': self.subjectId,
            'chapterName': self.chapterName,
            'description': self.description
        }
