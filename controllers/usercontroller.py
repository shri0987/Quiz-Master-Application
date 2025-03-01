import logging
import uuid
from flask import g, render_template, request, jsonify
from common.error import AppError
from models.admin import Admin, db
from services.userservice import UserService

class UserController:

    def __init__(self,app):
        self.app = app
        self.user_service = UserService()
        self.user_routes()

    def user_routes(self):

        @self.app.route('/user/login')
        def user_home():
            return render_template('userlogin.html')
        
        
        @self.app.route('/user/register')
        def user_register():
            return render_template('usercreate.html')


        @self.app.route('/v1/user/login', methods=['POST'])
        def user_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')

                logging.info(f'Login request for user {username}')

                if len(username) == 0 or username is None or len(password) == 0 or password is None:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)
                
                is_login_success = self.user_service.user_login(username, password)

                if not is_login_success:
                    raise AppError("Invalid credentials", AppError.INVALID_CREDENTIALS)
                    
                response = {"message": "Login successful"}
                return response, 200
            
            except AppError as e:
                error_details = e.to_dict()
                return render_template('userlogin.html', error_message = error_details["error"]), e.status_code

            except TimeoutError as e:
                return render_template('userlogin.html', error_message = "Operation Timed out"), 504

            except Exception as e:
                return render_template('userlogin.html', error_message = "Error occurred while processing login request"), 500
            

        @self.app.route('/v1/user/create', methods=['POST'])
        def user_create():
            try:
                create_request = request.form
                username = create_request.get('username')
                email = create_request.get('email')

                logging.info(f'Create user request for {username}')

                if len(username) == 0 or username is None or len(email) == 0 or email is None:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)

                user = self.user_service.create_user(create_request)

                if user is None:
                    raise AppError("User creation failed", AppError.INTERNAL_SERVER_ERROR)
                
                return render_template('userlogin.html', message = "User created successfully"), 201
                
            except AppError as e:
                error_details = e.to_dict()
                return render_template('usercreate.html', error_message = error_details["error"]), e.status_code
              
            except TimeoutError as e:    
                return render_template('usercreate.html', error_message = "Operation Timed out"), 504

            except Exception as e:
                return render_template('usercreate.html', error_message = "Error occurred while processing user create request"), 500