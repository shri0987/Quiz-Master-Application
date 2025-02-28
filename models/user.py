from repository.database import db

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.String(100), primary_key=True)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)  
    qualifications = db.Column(db.String(200), nullable=False)
    dateOfBirth = db.Column(db.String(200), nullable=False)
    createdOn = db.Column(db.DateTime, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    def __init__(self, userId, userName, email, password, name, phoneNumber, qualifications, dateOfBirth, createdOn, isActive):
        self.userId = userId
        self.userName = userName
        self.email = email
        self.password = password
        self.name = name
        self.phoneNumber = phoneNumber
        self.qualifications = qualifications
        self.dateOfBirth = dateOfBirth
        self.createdOn = createdOn
        self.isActive = isActive
    
    def _to_dict(self):
        return {
            'userId': self.userId,
            'userName': self.userName,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'phoneNumber': self.phoneNumber,
            'qualifications': self.qualifications,
            'dateOfBirth': self.dateOfBirth,
            'isActive': self.isActive,
            'createdOn': self.createdOn
        }