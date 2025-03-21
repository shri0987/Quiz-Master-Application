import re
import logging
import random
import string
import uuid
from flask import jsonify
import requests
from common.utility import Utility
from common.error import ApplicationError
from models.quiz import Quiz
from repository.quizrepository import QuizRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class QuizService:
    
    def __init__(self, app):
        self.app = app
        self.quiz_repository = QuizRepository()
        self.utility = Utility()


    def get_all_quizzes(self):
        try:
            logging.info("Fetching all quizzes")
            all_quizzes = self.quiz_repository.get_all_quizzes()
            
            if not all_quizzes:
                logging.info("No quizzes found")
                return []

            quizzes = [quiz.to_dict() for quiz in all_quizzes]
            return quizzes
        
        except Exception as e:
            logging.error("Error occured while fetching quizzes: %s", e)
            raise
    
    
    def get_quiz_by_id(self, quiz_id) -> Quiz:
        try:
            logging.info("Fetching quiz using quiz id %s", quiz_id)

            if not quiz_id:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)

            quiz = self.quiz_repository.get_quiz_by_id(quiz_id).to_dict()
            return quiz
        
        except Exception as e:
            logging.error("Error occured while fetching quiz by id: %s", e)
            raise
    

    def create_quiz(self, chapter_id, quiz_date, time_duration_minutes, remarks) -> Quiz:
        try:
            logging.info("Creating new quiz for chapter %s", chapter_id)

            base_url = self.app.config.get("URL")
            if not base_url:
                raise RuntimeError("Base URL is not set in app config")

            response = requests.get(f'{base_url}/api/v1/chapters/info/{chapter_id}')

            if response.status_code == 404:
                raise ApplicationError("Chapter not found", ApplicationError.CHAPTERS_NOT_FOUND)

            if response.status_code != 200:
                raise ApplicationError("Failed to fetch chapter", ApplicationError.INTERNAL_SERVER_ERROR)

            chapter_data = response.json()

            if not chapter_data:
                raise ApplicationError("Chapter data is empty", ApplicationError.CHAPTERS_NOT_FOUND)

            quiz_id = self.utility.generate_guid_id()
            quiz_name = str(chapter_data["chapterName"])

            new_quiz = Quiz(quiz_id, quiz_name, chapter_id, quiz_date, time_duration_minutes, remarks)

            created_quiz = self.quiz_repository.create_quiz(new_quiz)

            if created_quiz is None:
                return None
            return created_quiz
        
        except ApplicationError as e:  
            logging.error("Error occured while creating quiz: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while creating quiz: %s", e)
            raise


    def update_quiz(self, quiz_id, quizDate, chapter_id, timeDurationMinutes, remarks):
        try:
            logging.info("Updating new quiz for chapter %s", chapter_id)

            existing_quiz = self.get_quiz_by_id(quiz_id)

            if existing_quiz is None:
                raise ApplicationError("Subject does not exist", ApplicationError.SUBJECTS_NOT_FOUND)
            
            quiz_id = existing_quiz['quizId']
            quiz_name = existing_quiz['quizName']
            chapter_id = existing_quiz['chapterId']
            quiz_date = quizDate
            time_duration_minutes = timeDurationMinutes
            remarks = remarks

            modified_quiz = Quiz(quiz_id, quiz_name, chapter_id, quiz_date, time_duration_minutes, remarks)
            
            updated_quiz = self.quiz_repository.update_quiz(modified_quiz)

            if updated_quiz is None:
                return None
            return updated_quiz
        
        except ApplicationError as e:
            logging.error("Error occured while updating quiz: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while updating quiz: %s", e)
            raise

    
    def delete_quiz(self, quiz_id):
        try:
            logging.info("Deleting quiz with id %s", quiz_id)

            existing_quiz = self.get_quiz_by_id(quiz_id)

            if existing_quiz is None:
                raise ApplicationError("Quiz not found", ApplicationError.QUIZ_NOT_FOUND)

            deleted_quiz = self.quiz_repository.delete_quiz(quiz_id)

            if deleted_quiz is None:
                return None
            return deleted_quiz
        
        except ApplicationError as e:
            logging.error("Error occured while deleting quiz: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while deleting quiz: %s", e)
            raise