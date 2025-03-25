import logging
import requests
from common.error import ApplicationError
from services.quizservice import QuizService
from flask import redirect, render_template, request, jsonify, session, url_for

class QuizController:

    def __init__(self,app):
        self.app = app
        self.quiz_service = QuizService(app)
        self.quiz_api_routes()

    def quiz_api_routes(self):

        @self.app.route('/quiz', methods=['GET'])
        def render_quiz_dashboard():
            try: 
                username = session.get('admin_username')

                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))

                logging.info(f'Quiz dashboard request for {session.get('admin_username')}')

                base_url = self.app.config["URL"]
                response = requests.get(f'{base_url}/api/v1/quiz')

                if response.status_code != 200:
                    logging.error(f"Failed to fetch quiz: {response.text}")
                    return f"Error fetching quiz: {response.text}", response.status_code
                
                quiz_data = response.json()
                return render_template('quizdashboard.html', username = username , quizzes = quiz_data)
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing quiz dashboard request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing quiz dashboard request {e}"}), 500
         

        @self.app.route('/quiz/<quiz_id>', methods=['GET'])
        def render_quiz_page_by_id(quiz_id):
            try:
                username = session.get('admin_username')
                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))
                
                logging.info(f'Quiz page request for {quiz_id}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/api/v1/quiz/{quiz_id}')
                if response.status_code != 200:
                    logging.error(f"Failed to fetch quiz: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code

                quiz = response.json()

                response = requests.get(f'{base_url}/api/v1/question/{quiz_id}')
                if response.status_code != 200:
                    logging.error(f"Failed to fetch quiz: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code

                questions = response.json()

                return render_template('quizdetails.html', username = username, quiz = quiz, questions = questions)
               
            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return "Operation timed out", 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return "An error occurred while fetching the quiz page", 500

        
        @self.app.route('/quiz/create', methods=['GET'])
        def render_quiz_create_page(): 
            try:
                username = session.get('admin_username')
                logging.info(f'Quiz create page request by {username}')
                return render_template('createquizpage.html', username = username)
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('quizdashboard.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('quizdashboard.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('quizdashboard.html', error_message = "Error occured while processing create request"), 500


        @self.app.route('/quiz/<quiz_id>/info', methods=['GET'])  
        def render_quiz_info_page(quiz_id):
            try:
                username = session.get('admin_username')
                logging.info(f'Quiz page request for {quiz_id} by {username}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/api/v1/quiz/{quiz_id}')
                
                if response.status_code != 200:
                    logging.error(f"Failed to fetch quiz: {response.text}")
                    return f"Error fetching quiz: {response.text}", response.status_code
               
                quiz_data = response.json()

                return render_template('updatequizpage.html', quiz = quiz_data, username = username)

            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return "Operation timed out", 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return "An error occurred while fetching the quiz info page", 500
            

        @self.app.route('/<quiz_id>/view', methods = ['GET'])
        def render_user_quiz_view_page(quiz_id):
            try:
                username = session.get('user_username')
                logging.info(f'Quiz view page request for {quiz_id} by user {username}') 

                base_url = self.app.config.get("URL")
                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                response = requests.get(f'{base_url}/api/v1/quiz/{quiz_id}')
                
                if response.status_code != 200:
                    logging.error(f"Failed to fetch quiz information: {response.text}")
                    return f"Error fetching quiz information: {response.text}", response.status_code
               
                quiz_data = response.json()

                return render_template('viewquiz.html', quiz = quiz_data, username = username)

            except TimeoutError as e:
                logging.error(f"Timeout occurred: {e}", exc_info=True)
                return "Operation timed out", 504

            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                return "An error occurred while fetching the quiz info page", 500
            

        @self.app.route('/api/v1/quiz', methods=['GET'])
        def get_all_quizzes():
            try:
                logging.info(f'Request to fetch all quiz details') 

                all_quizzes = self.quiz_service.get_all_quizzes()

                if all_quizzes is None:
                    raise ApplicationError("Error occurred while fetching quizzes", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return jsonify(all_quizzes), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing quiz request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing quiz request {e}"}), 500

        
        @self.app.route('/api/v1/quiz/<quiz_id>', methods=['GET'])
        def get_quiz_by_id(quiz_id):
            try:
                quiz = self.quiz_service.get_quiz_by_id(quiz_id)

                if quiz is None:
                    raise ApplicationError("Quiz not found", ApplicationError.QUIZ_NOT_FOUND)
                
                return jsonify(quiz), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing quiz request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing quiz request {e}"}), 500


        @self.app.route('/api/v1/quiz/create', methods = ['POST'])
        def create_quiz():
            try:
                chapter_id = request.form.get('chapterId')
                quiz_date = request.form.get('quizDate')
                time_duration_minutes = int(request.form.get('timeDurationMinutes'))
                remarks = request.form.get('remarks')
                username = session.get('admin_username')

                logging.info(f'Create quiz for chapter {chapter_id} request by {username}')

                if not quiz_date or not time_duration_minutes:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                quiz = self.quiz_service.create_quiz(chapter_id, quiz_date, time_duration_minutes, remarks)

                if quiz is None:
                    raise ApplicationError("Error occurred while creating quiz", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return redirect(url_for('render_quiz_dashboard'))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('createquizpage.html', username = username, error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('createquizpage.html', username = username, error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('createquizpage.html', username = username, error_message = "Error occured while processing quiz create request"), 500
            

        @self.app.route('/api/v1/quiz/<quiz_id>/update', methods=['POST'])
        def update_quiz(quiz_id):
            try:
                chapter_id = request.form.get('chapterId')
                quizDate = request.form.get('quizDate')
                timeDurationMinutes = int(request.form.get('timeDurationMinutes'))
                remarks = request.form.get('remarks')
                username = session.get('admin_username')

                logging.info('session %s', session)

                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))

                logging.info(f'Quiz update request for {chapter_id} by user {username}')

                if not quizDate or not timeDurationMinutes or not remarks:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                quiz = self.quiz_service.update_quiz(quiz_id, quizDate, chapter_id, timeDurationMinutes, remarks)

                if quiz is None:
                    raise ApplicationError("Error occurred while updating quiz", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return redirect(url_for('render_quiz_page_by_id', quiz_id = quiz_id))

            except ApplicationError as e:
                error_details = e.to_dict()

            except TimeoutError:
                error_details = {"error": "Operation Timed out"}

            except Exception:
                error_details = {"error": "Error occurred while processing update request"}

            existing_quiz = self.quiz_service.get_quiz_by_id(quiz_id)
            
            if existing_quiz is None:
                return render_template('updatequizpage.html', error_message=error_details["error"]), 500

            return render_template('updatequizpage.html', quiz=existing_quiz, username = username, error_message=error_details["error"])
        

        @self.app.route('/api/v1/quiz/delete/<quiz_id>', methods = ['POST'])
        def delete_quiz(quiz_id):
            try:
                username = session.get('admin_username')
                if not username:
                    raise ApplicationError("Username is required", ApplicationError.INVALID_REQUEST)
                
                logging.info(f'Quiz delete request for {quiz_id} by {username}')

                if not quiz_id:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                quiz = self.quiz_service.delete_quiz(quiz_id)

                if quiz is None:
                    raise ApplicationError("Error occurred while deleting quiz", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return redirect(url_for('render_quiz_dashboard', username=username))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatequizpage.html', error_message = error_details["error"], quiz = quiz), e.status_code
            
            except TimeoutError as e:
                return render_template('updatequizpage.html', error_message = "Operation Timed out", quiz = quiz), 504
            
            except Exception as e:
                return render_template('updatequizpage.html', error_message = "Error occured while processing delete request", quiz = quiz), 500

        # quiz attempt controllers
        
        @self.app.route('/v1/quiz/<quiz_id>/attempt', methods=['GET'])
        def quiz(quiz_id):
            try:
                index = session.get('question_index')
                username = session.get('user_username')
                
                base_url = self.app.config.get("URL")

                if not base_url:
                    raise RuntimeError("Base URL is not set in app config")

                quiz_response = requests.get(f'{base_url}/api/v1/quiz/{quiz_id}')

                if quiz_response.status_code != 200:
                    return f"Error fetching quiz: {quiz_response.text}", quiz_response.status_code

                quiz_info = quiz_response.json()

                questions_response = requests.get(f'{base_url}/api/v1/question/{quiz_id}')

                if questions_response.status_code != 200:
                    return f"Error fetching questions: {questions_response.text}", questions_response.status_code
                
                question_list = questions_response.json()

                total_questions = len(question_list)

                if index >= total_questions:
                       session.pop('question_index')
                       # go to complete page which shows scores and contains back button to navigate to user page
                       return "Quiz Completed!", 200
                
                question = question_list[index]

                return render_template('displayquestion.html', quiz = quiz_info, question = question, index = index, total_questions = total_questions, username = username)
        
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing attempt request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing quiz attempt request {e}"}), 500


        @self.app.route('/v1/quiz/<quiz_id>/back', methods=['GET'])
        def previous_question(quiz_id):
            try:
                if session is None:
                    return redirect(url_for('user_login'))
                
                current_question_index = int(session['question_index'])

                if current_question_index <= 0:
                    session['question_index'] = 0
                else:
                    session['question_index'] = current_question_index - 1

                return redirect(url_for('quiz', quiz_id = quiz_id))
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": "Timeout error occurred while fetching previous question"}), 504
            
            except Exception as e:
                return jsonify({"error": "Error occurred while fetching previous question"}), 500
            

        @self.app.route('/api/v1/quiz/<quiz_id>/start', methods = ['GET'])
        def start_quiz(quiz_id):
            try:
                if session is None:
                    return redirect(url_for('user_login'))

                session['quiz_id'] = quiz_id
                session['question_index'] = 0
                
                logging.info(f'session {session['quiz_id']}')

                return redirect(url_for('quiz', quiz_id=quiz_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('userdashboard.html', error_message = error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('userdashboard.html', error_message = "Operation Timed out"), 504
            
            except Exception as e:
                return render_template('userdashboard.html', error_message = f"Error occured while processing delete request {e}"), 500


        @self.app.route('/api/v1/quiz/<quiz_id>/<question_id>/saveresponse', methods = ['POST'])
        def save_response(quiz_id, question_id):
            try:
                username = session.get('user_username')
                selectedOption = request.form.get('selected_option')

                if quiz_id is None or question_id is None:
                    raise ApplicationError('Invalid request', ApplicationError.INVALID_REQUEST)
                
                saved_response = self.quiz_service.save_response(quiz_id, question_id, username, selectedOption)

                if saved_response is None:
                    raise ApplicationError("Error occurred while saving response", ApplicationError.INTERNAL_SERVER_ERROR)
                
                session['question_index'] = int(session['question_index']) + 1
                return redirect(url_for('quiz', quiz_id = quiz_id))
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": "Timeout error occurred while saving response"}), 504
            
            except Exception as e:
                return jsonify({"error": "Error occurred while saving response"}), 500
            

        @self.app.route('/api/v1/quiz/<quiz_id>/submit', methods = ['POST'])
        def submit_quiz(quiz_id):
            try:
                # call service
                # fetch all responses and calculate final score
                # navigate to quiz 
                pass

            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": "Timeout error occurred while quiz submit"}), 504
            
            except Exception as e:
                return jsonify({"error": "Error occurred while quiz submit"}), 500
            