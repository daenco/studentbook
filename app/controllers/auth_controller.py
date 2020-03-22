from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_required, jwt_refresh_token_required, get_raw_jwt
)

from app.controllers.controller import Controller
from app.models.auth_model import AuthModel

from app.sys_utils.parsers import to_string

class RegistrationController(Resource, Controller):
    
    def __init__(self):
        super(RegistrationController, self).__init__()

        self.fields_to_get = {
            'username': to_string,
            'email': to_string,
            'password': to_string
        }

        self.auth_model = AuthModel()


    def post(self):
        self.get_fields_input(self.fields_to_get)
        self.auth_model.valid_user_no_exists(self.data_fields)
                                             
        result = self.auth_model.save_user(self.data_fields)
        access_token = create_access_token(identity=self.data_fields['username'])
        refresh_token = create_refresh_token(identity=self.data_fields['username'])

        result['access_token'] = access_token
        result['refresh_token'] = refresh_token

        self.request_info['result'] = result
        return self.request_info, result['status']


class LoginController(Resource, Controller):
    
    def __init__(self):
        super(LoginController, self).__init__()

        self.fields_to_get = {
            'username': to_string,
            'email': to_string,
            'password': to_string
        }

        self.auth_model = AuthModel()


    def post(self):
        self.get_fields_input(self.fields_to_get)
        user, status = self.auth_model.get_user(self.data_fields)

        self.request_info['result'] = {
            'access_token': create_access_token(identity=user[0]),
            'access_token': create_refresh_token(identity=user[0])
        }

        return self.request_info, status


class TokenRefreshController(Resource, Controller):
    
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        self.request_info['result'] = { 'access_token': access_token }
        return self.request_info, 200
        

class LogoutController(Resource, Controller):
    
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try: 
            with open('tokens.txt', 'w') as writer:
                writer.write(jti)

            self.request_info['result'] = { 'messaje': 'Access token has been revoked' }
            return self.request_info, 200
        except:
            self.request_info['result'] = { 'messaje': 'Something went wrong' }
            return self.request_info, 500
        

class LogoutRefreshController(Resource, Controller):
    
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            with open('tokens.txt', 'w') as writer:
                writer.write(jti)
                
            self.request_info['result'] = { 'messaje': 'Access token has been revoked' }
            return self.request_info, 200
        except:
            self.request_info['result'] = { 'messaje': 'Something went wrong' }
            return self.request_info, 500
        