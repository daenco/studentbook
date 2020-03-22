from datetime import timedelta

from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.controllers.auth_controller import (
    RegistrationController, LoginController, TokenRefreshController,
    LogoutController, LogoutRefreshController
)
from app.controllers.student_controller import StudentController
from app.controllers.department_controller import DepartmentController
from app.controllers.course_controller import CourseController

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'D4D0YNvlRzle0OkrpqEJ'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

api.add_resource(RegistrationController, '/registration')
api.add_resource(LoginController, '/login')
api.add_resource(TokenRefreshController, '/token/refresh')
api.add_resource(LogoutController, '/logout/access')
api.add_resource(LogoutRefreshController, '/logout/refresh')
api.add_resource(StudentController, '/students')
api.add_resource(DepartmentController, '/departments')
api.add_resource(CourseController, '/courses')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

    with open('tokens.txt', 'r') as reader:
        lines = reader.readlines()

    tokens = [line.rstrip() for line in lines]
    return jti in tokens

@app.route('/')
def index():
    response = make_response(jsonify({ 
        'resource': request.path,
        'message': 'OK'
    }), 200)

    response.headers['Content-Type'] = 'application/json'
    return response

@app.errorhandler(404)
def not_found(error):
    response = make_response(jsonify({ 
        'resource': request.path,
        'message': 'Error 404'  
    }), 404)

    response.headers['Content-Type'] = 'application/json'
    return response
