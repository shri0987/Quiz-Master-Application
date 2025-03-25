import sqlite3
import logging
from models.question import Question
logging.basicConfig(filename='app.log', level=logging.INFO)

class QuestionRepository:

    def get_question_by_id(self, question_id):
        try:
            logging.info("Fetching question with id %s", question_id)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = "SELECT * FROM questions WHERE questionId = ?"
            cursor.execute(query, (question_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return Question(*row)
            return None
        
        except sqlite3.Error as e:
            logging.error("Database error in fetch questions by id : %s", e)
            raise Exception("Database error occured while executing SQL query to fetch question")
        
        except Exception as e:
            logging.error("Error occurred while fetching question: %s", e)
            raise

    def get_questions_by_quiz_id(self, quiz_id):
        try:
            logging.info("Fetching questions for quiz id %s", quiz_id)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = "SELECT * FROM questions WHERE quizId = ?"
            cursor.execute(query, (quiz_id,))
            rows = cursor.fetchall()
            conn.close()
            return [Question(*row) for row in rows]
        
        except sqlite3.Error as e:
            logging.error("Database error in fetch questions by quiz id : %s", e)
            raise Exception("Database error occured while executing SQL query to fetch question")

        except Exception as e:
            logging.error("Error occurred while fetching questions: %s", e)
            raise

    def get_question_by_statement(self, question_statement):
        try:
            logging.info("Fetching question with statement %s", question_statement)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = "SELECT * FROM questions WHERE questionStatement = ?"
            cursor.execute(query, (question_statement,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return Question(*row)
            return None
        
        except sqlite3.Error as e:
            logging.error("Database error in fetch questions by statement : %s", e)
            raise Exception("Database error occured while executing SQL query to fetch question by statement")
        
        except Exception as e:
            logging.error("Error occurred while fetching question by statement: %s", e)
            raise

    def create_question(self, question):
        try:
            logging.info("Creating question %s", question.questionStatement)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = """
                INSERT INTO questions (questionId, quizId, questionStatement, option1, option2, option3, option4, correctOption, marks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                question.questionId,
                question.quizId,
                question.questionStatement,
                question.option1,
                question.option2,
                question.option3,
                question.option4,
                question.correctOption,
                question.marks
            ))

            conn.commit()
            conn.close()
            return question
        
        except Exception as e:
            logging.error("Error occurred while creating question: %s", e)
            raise

    def update_question(self, question):
        try:
            logging.info("Updating question %s", question.questionStatement)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = """
                UPDATE questions
                SET quizId = ?, questionStatement = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correctOption = ?, marks = ?
                WHERE questionId = ?
            """
            cursor.execute(query, (
                question.quizId,
                question.questionStatement,
                question.option1,
                question.option2,
                question.option3,
                question.option4,
                question.correctOption,
                question.marks,
                question.questionId
            ))
            conn.commit()
            conn.close()
            return question
        
        except Exception as e:
            logging.error("Error occurred while updating question: %s", e)
            raise

    def delete_question(self, question):
        try:
            question_id = question.questionId
            logging.info("Deleting question %s", question_id)
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            query = "DELETE FROM questions WHERE questionId = ?"
            cursor.execute(query, (question_id,))
            conn.commit()
            conn.close()
            return question
        
        except Exception as e:
            logging.error("Error occurred while deleting question: %s", e)
            raise