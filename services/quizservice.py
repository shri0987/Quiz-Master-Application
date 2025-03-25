import datetime
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
from models.response import Response
from repository.quizrepository import QuizRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class QuizService:
    
    def __init__(self, app):
        self.app = app
        self.quiz_repository = QuizRepository()
        self.utility = Utility()

    def is_valid_quiz(self, quiz: Quiz) -> bool:
        try:
            logging.info("Start validating quiz details")

            if not quiz:
                return False
            
            quiz_date = self.utility.get_date_object(str(quiz.quizDate))
            today_date = self.utility.get_current_date()

            if quiz_date < today_date:
                raise ApplicationError("Quiz date should be greater than or equal to today's date", ApplicationError.INVALID_REQUEST)
            
            minimum_quiz_duration = int(self.app.config.get("MINIMUM_QUIZ_DURATION"))

            if int(quiz.timeDurationMinutes) <= minimum_quiz_duration:
                raise ApplicationError(f"Time duration should be greater than {minimum_quiz_duration} minutes", ApplicationError.INVALID_REQUEST)

            maximum_quiz_duration = int(self.app.config.get("MAXIMUM_QUIZ_DURATION"))

            if int(quiz.timeDurationMinutes) > maximum_quiz_duration:
                raise ApplicationError(f"Time duration cannot be more than {maximum_quiz_duration} minutes", ApplicationError.INVALID_REQUEST)

            if not quiz.remarks:
                raise ApplicationError("Remark is required", ApplicationError.INVALID_REQUEST)
            
            return True

        except ApplicationError as e:  
            logging.error("Error occured while creating quiz: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while creating quiz: %s", e)
            raise


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

            is_valid_quiz = self.is_valid_quiz(new_quiz)

            if not is_valid_quiz:
                raise ApplicationError("Quiz details are not valid", ApplicationError.INVALID_REQUEST)

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
            time_duration_minutes = int(timeDurationMinutes)
            remarks = remarks

            modified_quiz = Quiz(quiz_id, quiz_name, chapter_id, quiz_date, time_duration_minutes, remarks)

            is_valid_quiz = self.is_valid_quiz(modified_quiz)

            if not is_valid_quiz:
                raise ApplicationError("Quiz details are not valid", ApplicationError.INVALID_REQUEST)
            
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
        

    def calculate_marks(self, question_id, selectedOption) -> int:
        try:
            logging.info('Start calculating marks for %s', question_id)
            scoredMarks = 0
            base_url = self.app.config.get("URL")
            if not base_url:
                raise RuntimeError("Base URL is not set in app config")

            response = requests.get(f'{base_url}/api/v1/question/info/{question_id}')

            if response.status_code == 404:
                raise ApplicationError("Question not found", ApplicationError.QUESTION_NOT_FOUND)

            if response.status_code != 200:
                raise ApplicationError("Failed to fetch question data", ApplicationError.INTERNAL_SERVER_ERROR)

            question_data = response.json()

            if not question_data:
                raise ApplicationError("Question data is empty", ApplicationError.QUESTION_NOT_FOUND)
            
            if str(question_data['correctOption']) == str(selectedOption):
                scoredMarks = question_data['marks']

            return scoredMarks
        
        except ApplicationError as e:  
            logging.error("Error occured while calculating marks: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while calculating marks: %s", e)
            raise
            
        
    def save_response(self, quiz_id, question_id, username, selectedOption):
        try:
            logging.info("Start saving response for question %s by user %s", question_id, username)

            # check attempt history and take decision to update existing response / create new one
            # based on quiz_id, question_id and username fetch data
            # if isVisited = True, means it has been visited so run update command instead of create
            
            calculatedMarks = self.calculate_marks(question_id, selectedOption)

            quiz_id = quiz_id
            question_id = question_id
            username = username
            user_response = selectedOption
            marks_scored = calculatedMarks
            attempt_time = self.utility.generate_current_datetime()
            is_question_visited = True

            response = Response(quiz_id, question_id, username, user_response, marks_scored, attempt_time, is_question_visited)

            saved_response = self.quiz_repository.save_user_response(response)

            if saved_response is None:
                return None
            
            return saved_response
        
        except ApplicationError as e:  
            logging.error("Error occured while creating quiz: %s", e)
            raise

        except Exception as e:
            logging.error("Error occured while creating quiz: %s", e)
            raise
            