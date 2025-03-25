import logging
import random
import re
import string
from flask import jsonify
from common.utility import Utility
from models.question import Question
from common.error import ApplicationError
from repository.questionrepository import QuestionRepository
logging.basicConfig(filename='app.log', level=logging.INFO)

class QuestionService:

    def __init__(self):
        self.question_repository = QuestionRepository()
        self.utility = Utility()


    def is_existing_question(self, question_statement) -> bool:
        try:
            logging.info("Fetching question with statement %s", question_statement)

            if not question_statement:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)

            question = self.question_repository.get_question_by_statement(question_statement)

            if question is None:
                return False
            return True

        except Exception as e:
            logging.error("Error occurred while fetching question: %s", e)
            raise


    def get_question_by_question_id(self, question_id) -> Question:
        try:
            logging.info("Fetching question %s", question_id)

            if not question_id:
                raise ApplicationError("Invalid Request", ApplicationError.INVALID_REQUEST)

            question = self.question_repository.get_question_by_id(question_id).to_dict()
            return question

        except Exception as e:
            logging.error("Error occurred while fetching question: %s", e)
            raise


    def get_questions_by_quiz_id(self, quiz_id) -> list:
        try:
            if not quiz_id:
                raise ApplicationError("Invalid request: quiz_id is required", ApplicationError.INVALID_REQUEST)

            logging.info("Fetching all questions using quiz id %s", quiz_id)

            questions = self.question_repository.get_questions_by_quiz_id(quiz_id)

            if not questions:
                logging.info("No questions found for quiz id %s", quiz_id)
                return []

            all_questions = [question.to_dict() for question in questions]
            return all_questions

        except ApplicationError as e:
            logging.error("ApplicationError occurred while fetching questions: %s", e)
            raise

        except Exception as e:
            logging.error("Unexpected error occurred while fetching questions: %s", e, exc_info=True)
            raise


    def create_question(self, quiz_id, question_statement, option1, option2, option3, option4, correct_option, marks) -> Question:
        try:
            logging.info("Creating new question %s", question_statement)

            question_id = self.utility.generate_guid_id()
          
            new_question = Question(questionId = question_id, quizId = quiz_id, questionStatement = question_statement,
                                    option1 = option1, option2 = option2, option3 = option3, option4 = option4,
                                    correctOption = correct_option, marks = marks)

            is_existing_question = self.is_existing_question(question_statement)

            if is_existing_question:
                raise ApplicationError("Question statement already exists", ApplicationError.QUESTION_EXISTS)

            created_question = self.question_repository.create_question(new_question)

            if created_question is None:
                return None
            return created_question

        except ApplicationError as e:
            logging.error("Error occurred while creating question: %s", e)
            raise

        except Exception as e:
            logging.error("Error occurred while creating question: %s", e)
            raise


    def update_question(self, quiz_id, question_id, question_statement, option1, option2, option3, option4, correct_option, marks) -> Question:
        try:
            logging.info("Update question %s", question_statement)

            existing_question = self.get_question_by_question_id(question_id)

            if existing_question is None:
                raise ApplicationError("Question does not exist", ApplicationError.QUESTION_NOT_FOUND)

            logging.info(f'question {jsonify(existing_question)}')

            question_id = existing_question['questionId']
            quiz_id = existing_question['quizId']
            question_statement = question_statement
            option1 = option1
            option2 = option2
            option3 = option3
            option4 = option4
            correct_option = correct_option
            marks = marks

            question = Question(
                questionId=question_id,
                quizId=quiz_id,
                questionStatement=question_statement,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correctOption=correct_option,
                marks=marks
            )

            updated_question = self.question_repository.update_question(question)

            if updated_question is None:
                return None
            return updated_question

        except ApplicationError as e:
            logging.error("Error occurred while updating question: %s", e)
            raise

        except Exception as e:
            logging.error("Error occurred while updating question: %s", e)
            raise

    
    def delete_question(self, question_id) -> Question:
        try:
            logging.info("Deleting question %s", question_id)

            if not question_id:
                raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)

            question_details = self.get_question_by_question_id(question_id)

            quiz_id = question_details.get('quizId')
            question_id = question_details.get('questionId')
            question_statement = question_details.get('questionStatement')
            option1 = question_details.get('option1')
            option2 = question_details.get('option2')
            option3 = question_details.get('option3')
            option4 = question_details.get('option4')
            correct_option = question_details.get('correctOption')
            marks = question_details.get('marks')

            question = Question(questionId = question_id, quizId = quiz_id, questionStatement = question_statement,
                                option1 = option1, option2 = option2, option3 = option3, option4 = option4,
                                correctOption = correct_option, marks = marks)

            if question is None:
                raise ApplicationError("Question does not exist", ApplicationError.QUESTION_NOT_FOUND)

            deleted_question = self.question_repository.delete_question(question)

            if deleted_question is None:
                return None
            return deleted_question

        except ApplicationError as e:
            logging.error("Error occurred while deleting question: %s", e)
            raise

        except Exception as e:
            logging.error("Error occurred while deleting question: %s", e)
            raise