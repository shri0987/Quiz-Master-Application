import logging
import requests
from common.error import ApplicationError
from models.chapter import Chapter, db
from services.chapterservice import ChapterService
from flask import redirect, render_template, request, jsonify, session, url_for

class ChapterController:

    def __init__(self, app):
        self.app = app
        self.chapter_service = ChapterService()
        self.chapter_api_routes()

    def chapter_api_routes(self):

        @self.app.route('/<subject_id>/chapters/<chapter_id>', methods=['GET'])
        def render_chapter_page(subject_id, chapter_id):
            try:
                base_url = self.app.config["URL"]
                response = requests.get(f'{base_url}/api/v1/chapters/info/{chapter_id}')

                if response.status_code != 200:
                    logging.error(f"Failed to fetch chapter: {response.text}")
                    return f"Error fetching chapter: {response.text}", response.status_code
                
                chapter_data = response.json()
                
                return render_template('updatechapterpage.html', chapter = chapter_data, username = session.get('admin_username'))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('subjectdetails.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('subjectdetails.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('subjectdetails.html', error_message = "Error occured while processing create request"), 500


        @self.app.route('/<subject_id>/chapters/create', methods=['GET'])
        def render_chapter_create_page(subject_id):
            try:
                return render_template('createchapterpage.html', subject_id = subject_id)
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('subjectdetails.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('subjectdetails.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('subjectdetails.html', error_message = "Error occured while processing create request"), 500
            
        
        @self.app.route('/api/v1/chapters/<subject_id>', methods=['GET'])
        def get_chapters_by_subject_id(subject_id):
            try:
                logging.info(f'Start fetching chapters using {subject_id}') 

                chapters = self.chapter_service.get_chapters_by_subject_id(subject_id)

                if chapters is None:
                    raise ApplicationError("Error occurred while fetching chapters", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return jsonify(chapters), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subject request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subject request {e}"}), 500


        @self.app.route('/api/v1/chapters/info/<chapter_id>', methods=['GET'])
        def get_chapter_by_chapter_id(chapter_id): 
            try:
                logging.info(f'Start fetching chapter {chapter_id}') 

                chapter = self.chapter_service.get_chapter_by_chapter_id(chapter_id)

                if chapter is None:
                    raise ApplicationError("Error occurred while fetching chapters", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return jsonify(chapter), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subject request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subject request {e}"}), 500


        @self.app.route('/api/v1/chapters/create', methods=['POST'])
        def create_chapter():
            try:
                subject_id = request.form.get('subjectId')
                chapter_name = request.form.get ('name')
                chapter_description = request.form.get('description')

                if chapter_name is None or chapter_description is None:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
               
                chapter = self.chapter_service.create_chapter(chapter_name, chapter_description, subject_id)

                if chapter is None:
                    raise ApplicationError("Error occurred while creating chapter", ApplicationError.INTERNAL_SERVER_ERROR)

                return redirect(url_for('render_subject_page', subject_id = subject_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('createchapterpage.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('createchapterpage.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('createchapterpage.html', error_message = "Error occured while processing create request"), 500
        

        @self.app.route('/api/v1/chapters/update', methods=['POST'])
        def update_chapter():
            try:
                subject_id = request.form.get('subjectId')
                chapter_id = request.form.get('chapterId')
                name = request.form.get('name')
                description = request.form.get('description')
                username = session.get('admin_username')
                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))

                logging.info(f'Start updating chapter {name} and id {chapter_id}')

                if not name or not description:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                chapter = self.chapter_service.update_chapter(subject_id, chapter_id, name, description)

                if chapter is None:
                    raise ApplicationError("Error occurred while creating chapter", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return redirect(url_for('render_subject_page', subject_id = subject_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatechapterpage.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('updatechapterpage.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('updatechapterpage.html', error_message = "Error occured while processing update request"), 500
            

        @self.app.route('/api/v1/chapters/delete/<chapter_id>', methods = ['POST'])
        def delete_chapter(chapter_id):
            chapter = None
            try:
                username = session.get('admin_username')
                if not username:
                    raise ApplicationError("Username is required", ApplicationError.INVALID_REQUEST)
                
                logging.info(f'Start deleting subject request {chapter_id} by {username}')

                if not chapter_id:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                chapter = self.chapter_service.delete_chapter(chapter_id)

                if chapter is None:
                    raise ApplicationError("Error occurred while deleting chapter", ApplicationError.INTERNAL_SERVER_ERROR)
                subject_id = chapter.get('subjectId')
                return redirect(url_for('render_subject_page', subject_id = subject_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatechapterpage.html', error_message = error_details["error"], chapter = chapter), e.status_code
            
            except TimeoutError as e:
                return render_template('updatechapterpage.html', error_message = "Operation Timed out", chapter = chapter), 504
            
            except Exception as e:
                return render_template('updatechapterpage.html', error_message = "Error occured while processing delete request", chapter = chapter), 500