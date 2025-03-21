import re
import uuid
import logging
from datetime import datetime
from models.admin import Admin
from common.error import ApplicationError
from repository.adminrepository import AdminRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class AdminService:
    
    def __init__(self):
        self.admin_repository = AdminRepository()

    def is_valid_username(self, username) -> bool:
        if not username:
            return False
        if len(username) < 3 or len(username) > 20:
            return False
        return True
    
    def admin_exists(self, username) -> bool:
        try:
            logging.info("Check existence of admin username %s", username)
            user = self.admin_repository.get_admin_by_username(username)
            if user is None:
                return False
            return True
        except Exception as e:
            logging.error("Error occured while checking user existence: %s", e)
            return False

    def admin_login(self, username, password) -> bool:
        try:
            if not self.is_valid_username(username):
                raise ApplicationError("Admin username is not valid", ApplicationError.VALIDATION_ERROR)
            
            logging.info("Fetching admin %s ", username)
            user = self.admin_repository.get_admin_by_username(username)
            if user is not None:
                if user._to_dict()['password'] == password:
                    return True
            else:         
                return False 

        except Exception as e:
            logging.error("Exception occured while fetching admin: %s", e)
            raise