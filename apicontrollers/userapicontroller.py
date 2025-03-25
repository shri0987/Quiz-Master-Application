import logging
import uuid
from flask import g, redirect, render_template, request, jsonify, session, url_for
import requests
from common.error import ApplicationError
from models.admin import Admin, db
from services.userservice import UserService

class UserController:

    def __init__(self,app):
        self.app = app
        self.user_service = UserService()
        self.user_api_routes()

    def user_api_routes(self):

        @self.app.route('/user/login')
        def render_user_login_page():
            return render_template('userlogin.html')
        
        
        @self.app.route('/user/register')
        def render_user_register_page():
            return render_template('usercreatepage.html')
        

        @self.app.route('/user/dashboard/<username>', methods=['GET'])
        def render_user_dashboard_page(username):
            try:
                logging.info(f'User dashboard request for user {session.get('admin_username')}') 
                base_url = self.app.config["URL"]
                quiz_response = requests.get(f'{base_url}/api/v1/quiz')

                if quiz_response.status_code != 200:
                    logging.error(f"Failed to fetch quiz details: {quiz_response.text}")
                    return f"Error fetching quiz: {quiz_response.text}", quiz_response.status_code
                
                quiz_data = quiz_response.json()

                return render_template('userdashboard.html', username=username, quizzes=quiz_data)
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing user dashboard request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing user dashboard request {e}"}), 500


        @self.app.route('/api/v1/user/login', methods=['POST'])
        def user_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')

                logging.info(f'Login request for user {username}')

                if len(username) == 0 or username is None or len(password) == 0 or password is None:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                is_user_login_success = self.user_service.user_login(username, password)

                if not is_user_login_success:
                    raise ApplicationError("Invalid credentials", ApplicationError.INVALID_CREDENTIALS)
                    
                session['user_username'] = username
                session['is_user_logged_in'] = True
            
                return redirect(url_for('render_user_dashboard_page', username = username))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('userlogin.html', error_message = error_details["error"]), e.status_code

            except TimeoutError as e:
                return render_template('userlogin.html', error_message = "Operation Timed out"), 504

            except Exception as e:
                return render_template('userlogin.html', error_message = "Error occurred while processing login request"), 500
            

        @self.app.route('/api/v1/user/create', methods=['POST'])
        def user_create():
            try:
                create_request = request.form
                username = create_request.get('username')
                email = create_request.get('email')

                logging.info(f'Create user request for {username}')

                if len(username) == 0 or username is None or len(email) == 0 or email is None:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)

                created_user = self.user_service.create_user(create_request)

                if created_user is None:
                    raise ApplicationError("User creation failed", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return render_template('userlogin.html', message = "User created successfully"), 201
                
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('usercreatepage.html', error_message = error_details["error"]), e.status_code
              
            except TimeoutError as e:    
                return render_template('usercreatepage.html', error_message = "Operation Timed out"), 504

            except Exception as e:
                return render_template('usercreatepage.html', error_message = "Error occurred while processing user create request"), 500