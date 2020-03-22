from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.controllers.controller import Controller
from app.models.student_model import StudentModel
from app.models.department_model import DepartmentModel

from app.sys_utils.parsers import to_string, to_integer, to_date, valid_index

class StudentController(Resource, Controller):
    
    def __init__(self):
        super(StudentController, self).__init__()

        self.fields_to_get = {
            'social_security_number': to_string,
            'first_name': to_string,
            'last_name': to_string,
            'date_of_birth': to_date,
            'sex': to_string,
            'current_address': to_string,
            'current_phone_number': to_string,
            'permanent_address': to_string,
            'permanent_phone_number': to_string,
            'class': to_string,
            'city': to_string,
            'state': to_string,
            'zip_code': to_integer,
        }

        self.list_filters = [ 'min_date', 'max_date', 'name', 'limit' ]

        self.student_number = valid_index(self.get_url_arg('student_number'))

        self.student_model = StudentModel()


    @jwt_required
    def get(self):
        if self.student_number:
            result = self.student_model.get_one(self.student_number, 
                                                DepartmentModel())
            self.request_info['result'] = result

            return self.request_info, result['status']
        else:
            str_filters = self.get_query_filters(self.list_filters)
            result = self.student_model.list_all(DepartmentModel(), 
                                                 str_filters=str_filters)
            self.request_info['result'] = result
            return self.request_info, result['status']


    @jwt_required
    def post(self):
        faked_students = self.get_url_arg('save_faked_students')

        if faked_students is not None:
            value = self.get_integer(faked_students)
            num_students = value if value is not None else 10
            result = self.student_model.save_faked_students(num_students,
                                                            DepartmentModel())
        else:
            self.get_fields_input(self.fields_to_get)
            result = self.student_model.save_one(self.data_fields, 
                                                self.get_url_arg('department_code'),
                                                student_number=self.student_number)
        self.request_info['result'] = result
        return self.request_info, result['status']


    @jwt_required
    def put(self):
        self.valid_required_arg('student_number')
        self.get_fields_input(self.fields_to_get)
        result = self.student_model.modify_one(self.data_fields, 
                                               self.student_number, 
                                               self.get_url_arg('current_department'),
                                               self.get_url_arg('new_department'))
        self.request_info['result'] = result
        return self.request_info, result['status']

    
    @jwt_required
    def delete(self):
        remove_all = self.get_url_arg('remove_all')

        if remove_all is not None and remove_all.lower() == 'true':
            result = self.student_model.clear_student_table()
        else:
            self.valid_required_arg('student_number')
            result = self.student_model.delete_one(self.student_number)

        self.request_info['result'] = result
        return self.request_info, result['status']
