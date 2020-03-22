from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.controllers.controller import Controller
from app.models.course_model import CourseModel
from app.models.department_model import DepartmentModel

from app.sys_utils.parsers import to_string, to_integer, to_date, valid_index

class CourseController(Resource, Controller):
    
    def __init__(self):
        super(CourseController, self).__init__()

        self.fields_to_get = {
            'name': to_string,
            'description': to_string,
            'semester_hours': to_integer,
            'course_level': to_integer
        }

        # self.list_filters = [ 'min_date', 'max_date', 'name', 'limit' ]

        self.course_number = valid_index(self.get_url_arg('course_number'))

        self.course_model = CourseModel()


    @jwt_required
    def get(self):
        if self.course_number:
            # DepartmentModel()
            result = self.course_model.get_one(self.course_number)
            self.request_info['result'] = result

            return self.request_info, result['status']
        else:
            # str_filters = self.get_query_filters(self.list_filters)
            result = self.course_model.list_all(DepartmentModel())
            self.request_info['result'] = result
            return self.request_info, result['status']


    @jwt_required
    def post(self):
        faked_courses = self.get_url_arg('save_faked_courses')
        self.valid_required_arg('department_code')

        if faked_courses is not None:
            value = self.get_integer(faked_courses)
            num_courses = value if value is not None else 6
            result = self.course_model.save_faked_courses(num_courses,
                                                          self.get_url_arg('department_code'))
        else:
            self.get_fields_input(self.fields_to_get)
            result = self.course_model.save_one(self.data_fields,
                                                self.get_url_arg('department_code'),
                                                student_number=self.student_number)
        self.request_info['result'] = result
        return self.request_info, result['status']


    # def put(self):
    #     self.valid_required_arg('student_number')
    #     self.get_fields_input(self.fields_to_get)
    #     result = self.student_model.modify_one(self.data_fields, 
    #                                            self.student_number, 
    #                                            self.get_url_arg('current_department'),
    #                                            self.get_url_arg('new_department'))
    #     self.request_info['result'] = result
    #     return self.request_info, result['status']

    
    @jwt_required
    def delete(self):
        remove_all = self.get_url_arg('remove_all')

        if remove_all is not None and remove_all.lower() == 'true':
            result = self.course_model.clear_course_table()
        else:
            self.valid_required_arg('course_number')
            result = self.course_model.delete_one(self.course_number)

        self.request_info['result'] = result
        return self.request_info, result['status']
