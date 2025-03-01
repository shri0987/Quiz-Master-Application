import re
import uuid
import logging
import random
import string
from datetime import datetime

from flask import jsonify
from common.utility import Utility
from models.subject import Subject
from common.error import AppError
from repository.subjectrepository import SubjectRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class SubjectService:
    
    def __init__(self):
        self.subject_repository = SubjectRepository()
        self.utility = Utility()

    def generate_subject_id(self, subject_name) -> str:
        prefix = subject_name[:3].upper()
        if len(prefix) < 3:
            prefix = prefix.ljust(3, 'X')
        random_number = ''.join(random.choices(string.digits, k=4))
        subject_id = f"{prefix}{random_number}"
        return subject_id
    
    def is_valid_subject_id(self, subject_id) -> bool:
        if not subject_id:
            return False
        if len(subject_id) < 3 or len(subject_id) > 20:
            return False
        if not re.match("^[A-Z]{3}[0-9]{4}$", subject_id):
            return False
        return True

    def get_all_subjects(self) -> list:
        try:
            logging.info("Fetching all subjects")
            subjects = self.subject_repository.get_all_subjects()
            all_subjects = [subject.to_dict() for subject in subjects]
            
            if len(all_subjects) == 0 or all_subjects is None:
                return None
            return all_subjects
        
        except Exception as e:
            logging.error("Error occured while fetching subjects: %s", e)
            raise

    def get_subject_by_id(self, subject_id) -> Subject:
        try:
            logging.info("Fetching subject %s", subject_id)

            if not subject_id:
                raise AppError("Invalid request", AppError.INVALID_REQUEST)
            
            if not self.is_valid_subject_id(subject_id):
                raise AppError("Invalid subject id", AppError.INVALID_REQUEST)

            subject = self.subject_repository.get_subject_by_id(subject_id)
            return subject
        
        except Exception as e:
            logging.error("Error occured while fetching subject: %s", e)
            raise

    def is_existing_subject(self, name) -> bool:
        try:
            logging.info("Fetching subject with name %s", name)

            if not name:
                raise AppError("Invalid request", AppError.INVALID_REQUEST)

            subject = self.subject_repository.get_subject_by_name(name)

            if subject is None:
                return False
            return True
                
        except Exception as e:
            logging.error("Error occured while fetching subject: %s", e)
            raise


    def create_subject(self, name, description) -> Subject:
        try:
            logging.info("Creating new subject %s", name)

            subject_id = self.generate_subject_id(name)
            created_on = self.utility.generate_current_datetime()
            new_subject = Subject(subject_id, name, description, created_on)

            is_existing_subject = self.is_existing_subject(name)

            if is_existing_subject == True:
                raise AppError("Subject name already exists", AppError.SUBJECT_EXISTS)

            created_subject = self.subject_repository.create_subject(new_subject)

            if created_subject is None:
                return None
            return created_subject
        
        except AppError as e:
            logging.error("Error occured while creating subject: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while creating subject: %s", e)
            raise
