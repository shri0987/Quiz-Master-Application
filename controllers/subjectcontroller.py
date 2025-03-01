import logging
import requests
from common.error import AppError
from models.admin import Admin, db
from services.subjectservice import SubjectService
from flask import flash, redirect, render_template, request, jsonify, session, url_for

class SubjectController:

    def __init__(self,app):
        self.app = app
        self.subject_service = SubjectService()
        self.subject_routes()

    def subject_routes(self):

        @self.app.route('/subjects/<subject_id>', methods=['GET'])
        def get_subject_page(subject_id):
            try:
                logging.info(f'Subject page request for {subject_id}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/v1/subjects/{subject_id}')
                
                if response.status_code != 200:
                    logging.error(f"Failed to fetch subject: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code

                subject_data = response.json()
                return render_template('subjectinfo.html', subject=subject_data)

            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return "Operation timed out", 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return "An error occurred while fetching the subject page", 500


        @self.app.route('/v1/subjects', methods=['GET'])
        def get_subjects():
            try:
                logging.info(f'Request to fetch all subjects') 

                all_subjects = self.subject_service.get_all_subjects()

                if all_subjects is None:
                    raise AppError("No subjects found", AppError.SUBJECTS_NOT_FOUND)
    
                return jsonify(all_subjects), 200
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subjects request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subjects request {e}"}), 500
            
            
        @self.app.route('/v1/subjects/<subject_id>', methods=['GET'])
        def get_subject_by_id(subject_id):
            try:
                logging.info(f'Start fetching subject using {subject_id}') 

                subject = self.subject_service.get_subject_by_id(subject_id)

                if subject is None:
                    raise AppError("Subject not found", AppError.SUBJECTS_NOT_FOUND)
                
                return jsonify(subject), 200
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing subject request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing subject request {e}"}), 500
            
        
        @self.app.route('/v1/subjects/create', methods=['POST'])
        def create_subject():
            try:
                name = request.form.get('name')
                description = request.form.get('description')

                logging.info(f'Start creating subject named {name}')

                if not name or not description:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)
                
                subject = self.subject_service.create_subject(name, description)

                if subject is None:
                    raise AppError("Error occurred while creating subject", AppError.INTERNAL_SERVER_ERROR)
                
                return jsonify({"message": "Subject created successfully"}), 201
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing create subject request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing create subject request {e}"}), 500
