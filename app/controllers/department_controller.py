from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.controllers.controller import Controller
from app.models.department_model import DepartmentModel
from app.models.student_model import StudentModel

from app.sys_utils.parsers import to_string, to_integer, to_date

class DepartmentController(Resource, Controller):

    def __init__(self):
        super(DepartmentController, self).__init__()

        self.fields_to_get = {
            'name': to_string,
            'office_number': to_integer,
            'office_phone': to_string,
            'college': to_string,
        }

        # self.list_filters = [ 'min_date', 'max_date', 'name', 'limit' ]

        self.department_code = self.get_url_arg('department_code')

        self.department_model = DepartmentModel()


    @jwt_required
    def get(self):
        if self.department_code:
            result = self.department_model.get_one(self.department_code,
                                                   StudentModel())
            self.request_info['result'] = result
            return self.request_info, result['status']
        else:
            # str_filters = self.get_query_filters(self.list_filters)
            # str_filters=str_filters
            result = self.department_model.list_all(StudentModel())
            self.request_info['result'] = result
            return self.request_info, result['status']


    @jwt_required
    def post(self):
        faked_departments = self.get_url_arg('save_faked_departments')

        if faked_departments is not None:
            num_departments = self.get_integer(faked_departments)
            result = self.department_model.save_faked_departments(num_departments 
                                                   if num_departments is not None 
                                                   else 10)
        else:
            self.get_fields_input(self.fields_to_get)
            result = self.department_model.save_one(self.data_fields,
                                                    department_code=self.department_code)
        self.request_info['result'] = result
        return self.request_info, result['status']


    @jwt_required
    def put(self):
        self.valid_required_arg('department_code')
        self.get_fields_input(self.fields_to_get)
        result = self.department_model.modify_one(self.data_fields, 
                                                  self.department_code)
        self.request_info['result'] = result
        return self.request_info, result['status']

    
    @jwt_required
    def delete(self):
        remove_all = self.get_url_arg('remove_all')

        if remove_all is not None and remove_all.lower() == 'true':
            result = self.department_model.clear_department_table()
        else:
            self.valid_required_arg('department_code')
            result = self.department_model.delete_one(self.department_code)

        self.request_info['result'] = result
        return self.request_info, result['status']
