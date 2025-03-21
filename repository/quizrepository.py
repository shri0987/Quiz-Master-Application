import sqlite3
import logging

from models.quiz import Quiz
logging.basicConfig(filename='app.log', level=logging.INFO) 

class QuizRepository:

    def get_all_quizzes(self) -> list:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT q.quizId, c.chapterId, q.quizDate, q.timeDurationMinutes, q.remarks, q.quizName 
            FROM quizzes as q
            INNER JOIN chapters as c
            ON q.chapterId = c.chapterId''')

            results = cursor.fetchall()
            
            quizzes = []
            for result in results:
                quiz_id, chapter_id, quiz_date, time_duration_minutes, remarks, quiz_name = result
                quiz = Quiz(quiz_id, quiz_name, chapter_id, quiz_date, time_duration_minutes, remarks)
                quizzes.append(quiz)

            logging.info("quizzes fetched successfully")
            return quizzes
                
        except sqlite3.Error as e:
            logging.error("SQLite error in fetch quizzes : %s", e)
            raise Exception("SQLite error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch quizzes : %s", e)
            raise Exception("Error occured in fetch quizzes")
        
        finally:
            conn.close()


    def get_quiz_by_id(self, quiz_id) -> Quiz:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quizzes WHERE quizId = ?", (quiz_id,))
            result = cursor.fetchone()

            if result:
                
                logging.info("Quiz %s fetched successfully", quiz_id)

                return Quiz(
                    quizId=result[0],
                    chapterId=result[1],
                    quizDate=result[2],
                    timeDurationMinutes=result[3],
                    remarks=result[4],
                    quizName=result[5]
                )
            
            return None 
                
        except sqlite3.Error as e:
            raise Exception("SQLite error occured while executing SQL query")
        
        except Exception as e:
            raise Exception("Error occured in fetch quiz")
        
        finally:
            conn.close()


    def create_quiz(self, quiz) -> Quiz:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quizzes VALUES (?, ?, ?, ?, ?, ?)", 
                            (quiz.quizId, quiz.chapterId, quiz.quizDate, quiz.timeDurationMinutes, quiz.remarks, quiz.quizName))
            conn.commit()
            logging.info("Quiz %s created successfully", quiz.quizName)
            return quiz
        
        except sqlite3.Error as e:
            raise Exception("SQLite error occured while executing SQL query")
        
        except Exception as e:
            raise Exception("Error occured in create quiz")
        
        finally:
            conn.close()


    def update_quiz(self, quiz) -> Quiz:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE quizzes SET chapterId = ?, quizDate = ?, timeDurationMinutes = ?, remarks = ?, quizName = ? WHERE quizId = ?", 
                            (quiz.chapterId, quiz.quizDate, quiz.timeDurationMinutes, quiz.remarks, quiz.quizName, quiz.quizId))
            conn.commit()

            if cursor.rowcount == 0:
                raise Exception(f"No quiz found with quiz id {quiz.quizId}")
            
            logging.info("Quiz %s updated successfully", quiz.quizName)
            
            return quiz
        
        except sqlite3.Error as e:
            raise Exception("SQLite error occured while executing SQL query", e)
        
        except Exception as e:
            raise Exception("Error occured in update quiz")
        
        finally:
            conn.close()

    
    def delete_quiz(self, quiz_id) -> str:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quizzes WHERE quizId = ?", (quiz_id,))

            if cursor.rowcount == 0:
                logging.error("No quiz found with quiz id: %s", quiz_id)
                return None
            conn.commit()

            logging.info("Quiz %s deleted successfully", quiz_id)
            return quiz_id
        
        except sqlite3.Error as e:
            raise Exception("SQLite error occured while executing SQL query")
        
        except Exception as e:
            raise Exception("Error occured in delete quiz")
        
        finally:
            conn.close()