import sqlite3
import logging
from models.user import User
logging.basicConfig(filename='app.log', level=logging.INFO) 

class UserRepository:
    
    def get_user_by_username(self, username) -> User:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE userName = ?", (username,))
            result = cursor.fetchone()
            if result is None:
                return None
            user = User(*result)
            logging.info("User %s fetched successfully", username)
            return user
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch user : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except TimeoutError as e:
            logging.error("Timeout error occured in fetch user by username: %s", e)
            raise Exception("Timeout error occured while fetch user")
        
        except Exception as e:
            logging.error("Error occured in fetch user : %s", e)
            raise Exception("Error occured in fetch user")
        
        finally:
            conn.close()

        
    def create_user(self, user) -> User:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (user.userId, user.userName, user.email, user.password, user.name, 
                            user.phoneNumber, user.qualifications, user.dateOfBirth, user.isActive, user.createdOn))
            conn.commit()
            logging.info("User %s created successfully", user.userName)
            return user
        
        except sqlite3.Error as e:
            logging.error("Database error occured in create user : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except TimeoutError as e:
            logging.error("Timeout error occured in create user : %s", e)
            raise Exception("Timeout error occured while creating user")
        
        except Exception as e:
            logging.error("Error occured in create user : %s", e)
            raise Exception("Error occured in create user")
        
        finally:
            conn.close()
