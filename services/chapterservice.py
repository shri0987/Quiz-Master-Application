import logging
import random
import re
import string
from flask import jsonify
from common.utility import Utility
from models.chapter import Chapter
from models.subject import Subject
from common.error import ApplicationError
from repository.chapterrepository import ChapterRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class ChapterService:
    
    def __init__(self):
        self.chapter_repository = ChapterRepository()
        self.utility = Utility()

    
    def generate_chapter_id(self, chapter_name, subject_id) -> str:
        prefix = chapter_name[:3].upper()
        subject_prefix = subject_id[:3].upper()
        if len(prefix) < 3:
            prefix = prefix.ljust(3, 'X')
        if len(subject_prefix) < 3:
            subject_prefix = subject_prefix.ljust(3, 'X')
        random_number = ''.join(random.choices(string.digits, k=4))
        chapter_id = subject_prefix + f"{prefix}{random_number}"
        return chapter_id
    
    def is_valid_chapter_id(self, chapter_id) -> bool:
        if not chapter_id:
            return False
        if len(chapter_id) < 3 or len(chapter_id) > 20:
            return False
        if not re.match("^[A-Z]{6}[0-9]{4}$", chapter_id):
            return False
        return True

    def is_existing_chapter(self, name) -> bool:
        try:
            logging.info("Fetching chapter with name %s", name)

            if not name:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)

            chapter = self.chapter_repository.get_chapter_by_name(name)

            if chapter is None:
                return False
            return True
                
        except Exception as e:
            logging.error("Error occured while fetching subject: %s", e)
            raise

    def get_chapter_by_chapter_id(self, chapter_id) -> Chapter:
        try:
            logging.info("Fetching chapter %s", chapter_id)

            if not chapter_id:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
            
            if not self.is_valid_chapter_id(chapter_id):
                raise ApplicationError("Invalid chapter id", ApplicationError.INVALID_REQUEST)

            chapter = self.chapter_repository.get_chapter_by_id(chapter_id).to_dict()
            return chapter
        
        except Exception as e:
            logging.error("Error occured while fetching chapter: %s", e)
            raise

    def get_chapters_by_subject_id(self, subject_id) -> list:
        try:
            if not subject_id:
                raise ApplicationError("Invalid request: subject_id is required", ApplicationError.INVALID_REQUEST)
            
            logging.info("Fetching all chapters using subject id %s", subject_id)
            
            chapters = self.chapter_repository.get_chapters_by_subject_id(subject_id)
            
            if not chapters:
                logging.info("No chapters found for subject id %s", subject_id)
                return []

            all_chapters = [chapter.to_dict() for chapter in chapters]
            return all_chapters
        
        except ApplicationError as e:
            logging.error("ApplicationError occurred while fetching chapters: %s", e)
            raise
        
        except Exception as e:
            logging.error("Unexpected error occurred while fetching chapters: %s", e, exc_info=True)
            raise

    def create_chapter(self, chapter_name, chapter_description, subject_id) -> Chapter:
        try:
            logging.info("Creating new chapter %s", chapter_name)

            chapter_id = self.generate_chapter_id(chapter_name, subject_id)
            created_on = self.utility.generate_current_datetime()
            new_chapter = Chapter(chapter_id, subject_id, chapter_name, chapter_description, created_on)

            is_existing_chapter = self.is_existing_chapter(chapter_name)

            if is_existing_chapter == True:
                raise ApplicationError("Chapter name already exists", ApplicationError.CHAPTER_EXISTS)

            created_chapter = self.chapter_repository.create_chapter(new_chapter)

            if created_chapter is None:
                return None
            return created_chapter
        
        except ApplicationError as e:
            logging.error("Error occured while creating chapter: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while creating chapter: %s", e)
            raise
    
    def update_chapter(self, subject_id, chapter_id, name, description) -> Chapter:
        try:
            logging.info("Update chapter %s", name)

            existing_chapter = self.get_chapter_by_chapter_id(chapter_id)

            if existing_chapter is None:
                raise ApplicationError("Subject does not exist", ApplicationError.SUBJECTS_NOT_FOUND)
            
            logging.info(f'chapter {jsonify(existing_chapter)}')
            
            subject_id = existing_chapter['subjectId']
            chapter_id = existing_chapter['chapterId']
            name = existing_chapter['chapterName']
            description = description
            created_on = existing_chapter['createdOn']

            chapter = Chapter(chapter_id, subject_id, name, description, created_on)

            updated_chapter = self.chapter_repository.update_chapter(chapter)

            if updated_chapter is None:
                return None
            return updated_chapter
        
        except ApplicationError as e:
            logging.error("Error occured while updating chapter: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while updating chapter: %s", e)
            raise

    def delete_chapter(self, chapter_id) -> Chapter:
        try:
            logging.info("Deleting chapter %s", chapter_id)

            if not chapter_id:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
            
            if not self.is_valid_chapter_id(chapter_id):
                raise ApplicationError("Invalid chapter id", ApplicationError.INVALID_REQUEST)
            
            chapter = self.get_chapter_by_chapter_id(chapter_id) 
            
            if chapter is None:
                raise ApplicationError("Chapter does not exist", ApplicationError.CHAPTERS_NOT_FOUND)

            deleted_chapter = self.chapter_repository.delete_chapter(chapter)

            if deleted_chapter is None:
                return None
            return deleted_chapter
            
        except ApplicationError as e:
            logging.error("Error occured while deleting chapter: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while deleting chapter: %s", e)
            raise