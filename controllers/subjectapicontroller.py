import logging
import requests
from common.error import ApplicationError
from models.admin import Admin, db
from services.subjectservice import SubjectService
from flask import redirect, render_template, request, jsonify, session, url_for

class SubjectController:

    def __init__(self,app):
        self.app = app
        self.subject_service = SubjectService()
        self.subject_api_routes()

    def subject_api_routes(self):

        @self.app.route('/subjects/<subject_id>', methods=['GET'])
        def render_subject_page(subject_id):
            try:
                logging.info(f'Subject page request for {subject_id}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/api/v1/subjects/{subject_id}')
                if response.status_code != 200:
                    logging.error(f"Failed to fetch subject: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code

                subject_data = response.json()

                chapter_response = requests.get(f'{base_url}/api/v1/chapters/{subject_id}')
                if chapter_response.status_code != 200:
                    logging.error(f"Failed to fetch chapters: {chapter_response.text}")
                    return f"Error fetching chapters: {chapter_response.text}", chapter_response.status_code
                
                chapter_data = chapter_response.json()
                if chapter_data is None:
                    chapter_data = []

                return render_template('subjectdetails.html', subject=subject_data, chapters=chapter_data, username = session.get('admin_username'))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('admindashboard.html', error_message = error_details["error"]), e.status_code

            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return render_template('admindashboard.html', error_message = "Operation timed out"), 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return render_template('admindashboard.html', error_message = "Operation timed out"), 500


        @self.app.route('/subjects/<subject_id>/info', methods=['GET'])
        def render_subject_info_page(subject_id):
            try:
                logging.info(f'Subject page request for {subject_id}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/api/v1/subjects/{subject_id}')
                
                if response.status_code != 200:
                    logging.error(f"Failed to fetch subject: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code
               
                subject_data = response.json()
                username = session.get('admin_username')

                return render_template('updatesubjectpage.html', subject = subject_data, username = username)

            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return "Operation timed out", 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return "An error occurred while fetching the subject info page", 500


        @self.app.route('/subjects/create', methods=['GET'])
        def render_subject_create_page():
            try:
                return render_template('createsubjectpage.html')
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('admindashboard.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('admindashboard.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('admindashboard.html', error_message = "Error occured while processing create request"), 500


        @self.app.route('/api/v1/subjects', methods=['GET'])
        def get_all_subjects():
            try:
                username = session.get('admin_username')
                logging.info('Request to fetch all subjects by user %s', username) 

                all_subjects = self.subject_service.get_all_subjects()

                if all_subjects is None:
                    raise ApplicationError("Error occurred while fetching subjects", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return jsonify(all_subjects), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subjects request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subjects request {e}"}), 500
              
            
        @self.app.route('/api/v1/subjects/<subject_id>', methods=['GET'])
        def get_subject_by_id(subject_id):
            try:
                logging.info(f'Start fetching subject using {subject_id}') 

                subject = self.subject_service.get_subject_by_id(subject_id)

                if subject is None:
                    raise ApplicationError("Subject not found", ApplicationError.SUBJECTS_NOT_FOUND)
                
                return jsonify(subject), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subject request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subject request {e}"}), 500
            
        
        @self.app.route('/api/v1/subjects/create', methods=['POST'])
        def create_subject():
            try:
                name = request.form.get('name')
                description = request.form.get('description')
                username = session.get('admin_username')

                logging.info(f'Create subject {name} request by {username}')

                if not name or not description:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                subject = self.subject_service.create_subject(name, description)

                if subject is None:
                    raise ApplicationError("Error occurred while creating subject", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return redirect(url_for('render_admin_dashboard_page', username=username))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('createsubjectpage.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('createsubjectpage.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('createsubjectpage.html', error_message = "Error occured while processing create request"), 500


        @self.app.route('/api/v1/subject/update', methods=['POST'])
        def update_subject():
            try:
                id = request.form.get('id')
                name = request.form.get('name')
                description = request.form.get('description')
                username = session.get('admin_username')
                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))

                logging.info(f'Start updating subject named {name} and id {id}')

                if not name or not description:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                subject = self.subject_service.update_subject(id, name, description)

                if subject is None:
                    raise ApplicationError("Error occurred while creating subject", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return redirect(url_for('render_subject_page', subject_id=id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatesubjectpage.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('updatesubjectpage.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('updatesubjectpage.html', error_message = "Error occured while processing update request"), 500


        @self.app.route('/api/v1/subjects/delete/<subject_id>', methods = ['POST'])
        def delete_subject(subject_id): 
            subject = None
            try:
                username = session.get('admin_username')
                if not username:
                    raise ApplicationError("Username is required", ApplicationError.INVALID_REQUEST)
                
                logging.info(f'Start deleting subject request {subject_id} by {username}')

                if not subject_id:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                subject = self.subject_service.delete_subject(subject_id)

                if subject is None:
                    raise ApplicationError("Error occurred while deleting subject", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return redirect(url_for('render_admin_dashboard_page', username=username))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatesubjectpage.html', error_message = error_details["error"], subject = subject), e.status_code
            
            except TimeoutError as e:
                return render_template('updatesubjectpage.html', error_message = "Operation Timed out", subject = subject), 504
            
            except Exception as e:
                return render_template('updatesubjectpage.html', error_message = "Error occured while processing delete request", subject = subject), 500