import sqlite3
import logging
from models.chapter import Chapter
logging.basicConfig(filename='app.log', level=logging.INFO) 

class ChapterRepository:

    def get_chapter_by_id(self, chapter_id) -> Chapter:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chapters WHERE chapterId = ?", (chapter_id,))
            result = cursor.fetchone()

            if result is None:
                return None
            
            chapter = Chapter(*result)
            logging.info("Chapter %s fetched successfully", chapter_id)
            return chapter
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch chapter : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch chapter : %s", e)
            raise Exception("Error occured in fetch chapter")
        
        finally:
            conn.close()
    
    def get_chapter_by_name(self, name) -> Chapter:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chapters WHERE chapterName = ?", (name,))
            result = cursor.fetchone()

            if result is None:
                return None
            
            chapter = Chapter(*result)
            logging.info("Chapter %s fetched successfully", name)
            return chapter
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch chapter using name : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch chapter using name : %s", e)
            raise Exception("Error occured in fetch subject")
        
        finally:
            conn.close()

    def get_chapters_by_subject_id(self, subject_id) -> list:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chapters WHERE subjectId = ?", (subject_id,))
            results = cursor.fetchall()
            
            chapters = []
            for result in results:
                chapter = Chapter(*result)
                chapters.append(chapter)

            logging.info("Chapters fetched successfully")
            return chapters
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch chapters : %s", e)
            raise Exception("Database error occured while executing SQL query to fetch chapters")
        
        except Exception as e:
            logging.error("Error occured in fetch chapters : %s", e)
            raise Exception("Error occured in fetch chapters")
        
        finally:
            conn.close()

    def create_chapter(self, chapter) -> Chapter:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chapters VALUES (?, ?, ?, ?, ?)", 
                            (chapter.chapterId, chapter.subjectId, chapter.chapterName, chapter.description, chapter.createdOn))
            conn.commit()
            logging.info("Chapter %s created successfully", chapter.chapterName)
            return chapter
        
        except sqlite3.Error as e:
            logging.error("Database error occured in create chapter : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in create chapter : %s", e)
            raise Exception("Error occured in create chapter")
        
        finally:
            conn.close()

    def update_chapter(self, chapter) -> Chapter:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE chapters SET chapterId = ?, subjectId = ?, chapterName = ?, description = ?, createdOn = ? WHERE chapterId = ?",
                          (chapter.chapterId, chapter.subjectId, chapter.chapterName, chapter.description, chapter.createdOn, chapter.chapterId))
            conn.commit()

            if cursor.rowcount == 0:
                raise Exception(f"No subject found with chapter Id {chapter.chapterId}")

            logging.info("Chapter %s updated successfully", chapter.chapterId)
            return chapter

        except sqlite3.Error as e:
            logging.error("Database error occurred in update chapter: %s", e)
            raise Exception("Database error occurred while executing SQL query")

        except Exception as e:
            logging.error("Error occurred in update chapter: %s", e)
            raise Exception("Error occurred in update chapter")

        finally:
            conn.close()

    def delete_chapter(self, chapter) -> Chapter:
        try:
            chapter_id = chapter.get('chapterId')
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chapters WHERE chapterId = ?", (chapter_id,))

            if cursor.rowcount == 0:
                logging.error("No chapter found with id: %s", chapter_id)
                return None
            conn.commit()

            logging.info("Chapter %s deleted successfully", chapter_id)
            return chapter

        except sqlite3.Error as e:
            logging.error("Database error in delete chapter using name: %s", e)
            raise Exception("Database error occurred while executing SQL query")

        except Exception as e:
            logging.error("Error occurred in delete chapter using name: %s", e)
            raise Exception("Error occurred in delete subject")

        finally:
            conn.close()