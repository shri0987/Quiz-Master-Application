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

        @self.app.route('/v1/subjects', methods=['GET'])
        def get_subjects():
            try:
                logging.info(f'Fetching subjects') 

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
        def get_subject(subject_id):
            try:
                logging.info(f'Fetching subject {subject_id}') 

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

                logging.info(f'Creating subject {name}')

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
