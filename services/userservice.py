import re
import uuid
import logging
from datetime import datetime
from models.user import User
from common.error import AppError
from repository.userrepository import UserRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def generate_user_id(self) -> str:
        return str(uuid.uuid4())
    
    def generate_current_datetime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_valid_username(self, username) -> bool:
        if not username:
            return False
        if len(username) < 3 or len(username) > 20:
            return False
        return True
    
    def is_valid_email(self, email) -> bool:
        if not email:
            return False
        if len(email) < 3 or len(email) > 50:
            return False
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return False
        return True
    
    def is_valid_phone_number(self, phone_number) -> bool:
        if not phone_number:
            return False
        if len(phone_number) < 10 or len(phone_number) > 15:
            return False
        if not re.match(r'^[0-9]+$', phone_number):
            return False
        return True
    
    def validate_user_creation_request(self, create_request) -> bool:
        if (create_request.get('username') is None or create_request.get('password') is None or 
            create_request.get('email') is None or create_request.get('phone') is None or 
            create_request.get('name') is None or create_request.get('qualifications') is None or 
            create_request.get('dob') is None):
            return False
        else:
            if (not self.is_valid_username(create_request.get('username')) or 
                not self.is_valid_email(create_request.get('email')) or 
                not self.is_valid_phone_number(create_request.get('phone'))):
                return False
            logging.info("User details are valid")
            return True
        
    def user_exists(self, username) -> bool:
        try:
            logging.info("Check existence of username %s", username)
            user = self.user_repository.get_user_by_username(username)
            if user is None:
                return False
            return True
        except Exception as e:
            logging.error("Error occured while checking user existence: %s", e)
            return False

    def user_login(self, username, password) -> bool:
        try:
            if not self.is_valid_username(username):
                raise AppError("Username is not valid", AppError.VALIDATION_ERROR)
            
            if not self.user_exists(username):
                raise AppError("User not found", AppError.USER_NOT_FOUND)
            
            logging.info("Fetching user %s ", username)
            user = self.user_repository.get_user_by_username(username)
            if user is not None:
                if user._to_dict()['password'] == password:
                    return True
            else:         
                return False 

        except Exception as e:
            logging.error("Exception occured while fetching user: %s", e)
            raise
        
    def create_user(self, create_request) -> User:
        try:
            username = create_request.get('username')
            email = create_request.get('email')
            password = create_request.get('password')
            name = create_request.get('name')
            phoneNumber = create_request.get('phone')
            qualifications = create_request.get('qualifications')
            dateOfBirth = create_request.get('dob')
            isActive = True

            if not self.validate_user_creation_request(create_request):
                raise AppError("User details are not valid", AppError.VALIDATION_ERROR)

            if self.user_exists(username):
                raise AppError("User already exists", AppError.USER_EXISTS)

            logging.info("Start creating user %s", create_request.get('username'))
            user_id = self.generate_user_id()
            created_on = self.generate_current_datetime()
            new_user = User(user_id, username, email, password, name, phoneNumber, qualifications, dateOfBirth, created_on, isActive)
            created_user = self.user_repository.create_user(new_user)
            if created_user is not None:
                return created_user
            else:
                return None

        except Exception as e:
            logging.error("Error occured while creating user: %s", e)
            raise