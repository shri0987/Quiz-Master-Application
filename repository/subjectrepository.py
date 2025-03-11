import sqlite3
import logging
from models.subject import Subject
logging.basicConfig(filename='app.log', level=logging.INFO) 

class SubjectRepository:

    def get_all_subjects(self) -> list:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects")
            results = cursor.fetchall()
            
            subjects = []
            for result in results:
                subject = Subject(*result)
                subjects.append(subject)

            logging.info("Subjects fetched successfully")
            return subjects
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch subjects : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch subjects : %s", e)
            raise Exception("Error occured in fetch subjects")
        
        finally:
            conn.close()

    def create_subject(self, subject) -> Subject:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subjects VALUES (?, ?, ?, ?)", 
                            (subject.subjectId, subject.subjectName, subject.description, subject.createdOn))
            conn.commit()
            logging.info("Subject %s created successfully", subject.subjectName)
            return subject
        
        except sqlite3.Error as e:
            logging.error("Database error occured in create subject : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in create subject : %s", e)
            raise Exception("Error occured in create subject")
        
        finally:
            conn.close()

    def get_subject_by_id(self, subject_id) -> Subject:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects WHERE subjectId = ?", (subject_id,))
            result = cursor.fetchone()

            if result is None:
                return None
            
            subject = Subject(*result)
            logging.info("Subject %s fetched successfully", subject_id)
            return subject
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch subject : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch subject : %s", e)
            raise Exception("Error occured in fetch subject")
        
        finally:
            conn.close()

    
    def get_subject_by_name(self, name) -> Subject:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects WHERE subjectName = ?", (name,))
            result = cursor.fetchone()

            if result is None:
                return None
            
            subject = Subject(*result)
            logging.info("Subject %s fetched successfully", name)
            return subject
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch subject using name : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch subject using name : %s", e)
            raise Exception("Error occured in fetch subject")
        
        finally:
            conn.close()

    def update_subject(self, subject) -> Subject:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE subjects SET subjectName = ?, description = ?, createdOn = ? WHERE subjectId = ?",
                          (subject.subjectName, subject.description, subject.createdOn, subject.subjectId))
            conn.commit()

            if cursor.rowcount == 0:
                logging.warning("No subject found with subjectId %s", subject.subjectId)
                raise Exception(f"No subject found with subjectId {subject.subjectId}")

            logging.info("Subject %s updated successfully", subject.subjectId)
            return subject

        except sqlite3.Error as e:
            logging.error("Database error occurred in update subject: %s", e)
            raise Exception("Database error occurred while executing SQL query")

        except Exception as e:
            logging.error("Error occurred in update subject: %s", e)
            raise Exception("Error occurred in update subject")

        finally:
            conn.close()


    def delete_subject(self, subject_id) -> str:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subjectId = ?", (subject_id,))

            if cursor.rowcount == 0:
                logging.error("No subject found with id: %s", subject_id)
                return None
            conn.commit()

            logging.info("Subject %s deleted successfully", subject_id)
            return subject_id

        except sqlite3.Error as e:
            logging.error("Database error in delete subject using name: %s", e)
            raise Exception("Database error occurred while executing SQL query")

        except Exception as e:
            logging.error("Error occurred in delete subject using name: %s", e)
            raise Exception("Error occurred in delete subject")

        finally:
            conn.close()
