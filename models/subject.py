from datetime import datetime
from repository.database import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    subjectId = db.Column(db.String, primary_key=True, nullable=False)
    subjectName = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    createdOn = db.Column(db.DateTime)

    def __init__(self, subjectId, subjectName, description, createdOn):
        self.subjectId = subjectId
        self.subjectName = subjectName
        self.description = description
        self.createdOn = createdOn

    def to_dict(self):
        return {
            'subjectId': self.subjectId,
            'subjectName': self.subjectName,
            'description': self.description,
            'createdOn': self.createdOn
        }
