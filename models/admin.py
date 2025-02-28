from repository.database import db

class Admin(db.Model):
    __tablename__ = 'admins'
    adminId = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, adminId, name, phoneNumber, email, userName, password):
        self.adminId = adminId
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email
        self.userName = userName
        self.password = password

    def _to_dict(self):
        return {
            'adminId': self.adminId,
            'name': self.name,
            'phoneNumber': self.phoneNumber,
            'email': self.email,
            'userName': self.userName,
            'password': self.password
        }