from datetime import datetime
from random import randint

from faker import Faker

from app.models.model import Model

class DepartmentModel(Model):

    def __init__(self):
        super(DepartmentModel, self).__init__()

        self.columns = {
            'department.code': 'department_code',
            'department.name': 'department_name',
            'department.office_number': 'office_number',
            'department.office_phone': 'office_phone',
            'department.college': 'college',
        }

        self.set_query_columns(self.columns)

    
    def list_all(self, student_model, str_filters=''):
        line = '''  SELECT 
                        {columns} 
                    FROM department
                    WHERE department.status = TRUE {str_filters}'''
        query = line.format(columns=self.get_query_columns_string(),
                            str_filters=str_filters)
        self.add_query_to_execute(query)
        departments = self.get_full_list()
        departments_data = departments['data']

        if len(departments_data):
            students = student_model.get_students()
            departments['data'] = self.get_all_departments_students(departments_data, students)

        return departments

    
    def get_one(self, department_code, student_model):
        line =  """ SELECT 
                        {columns} 
                    FROM department
                    WHERE code = '{department_code}'
                    AND department.status = TRUE"""
        query = line.format(columns=self.get_query_columns_string(),
                            department_code=department_code)
        self.add_query_to_execute(query)

        department = self.get_one_row()
        department_data = department['data']

        if len(department_data):
            students = student_model.get_students(department_code)
            department['data'] = self.get_one_department_students(department_data, 
                                                                  students)

        return department


    def save_one(self, data_fields, **kwargs):
        department_code = self.get_index(kwargs.get('department_code'))

        line = """  INSERT INTO department
                    VALUES (
                        '{code}',
                        '{name}',
                        '{office_number}',
                        '{office_phone}',
                        '{college}'
                    )"""
        query = line.format(code=department_code, **data_fields)
        self.add_query_to_execute(query)

        return self.execute_query()

    
    def save_faked_departments(self, number_departments):
        fake = Faker()

        for _ in range(0, number_departments):
            department_code = self.get_uuid()

            line = """  INSERT INTO department
                        VALUES (
                            '{code}',
                            '{name}',
                            '{office_number}',
                            '{office_phone}',
                            '{college}'
                        )"""
            query = line.format(code=department_code,
                                name=fake.company(),
                                office_number=randint(1, 99),
                                office_phone=fake.phone_number(),
                                college=fake.bs())
            self.add_query_to_execute(query)

        return self.execute_queries()


    def modify_one(self, data_fields, department_code):
        self.valid_department_exists(department_code)

        line = """  UPDATE department
                    SET name = '{name}',
                        office_number = {office_number},
                        office_phone = '{office_phone}',
                        college = '{college}'
                    WHERE code = '{department_code}'
                    AND status = TRUE"""
        query = line.format(department_code=department_code, **data_fields)
        self.add_query_to_execute(query)

        return self.execute_query()


    def delete_one(self, department_code):
        self.valid_department_exists(department_code)

        line = """UPDATE department 
                  SET status = FALSE 
                  WHERE code = '{department_code}'
                  AND status = TRUE"""
        query = line.format(department_code=department_code)
        self.add_query_to_execute(query)
        self.remove_all_students(department_code)

        return self.execute_queries()


    def clear_department_table(self):
        self.add_query_to_execute("DELETE FROM student_department")
        self.add_query_to_execute("DELETE FROM department")
        
        return self.execute_queries()

    
    def get_departments(self, student_number=None):
        query = ''' SELECT 
                        student_department.student_number,
                        student_department.department_code,
                        student_department.status,
                        department.name
                    FROM department
                    JOIN student_department ON department.code = student_department.department_code
                    WHERE department.status = TRUE
                    AND student_department.status = TRUE'''

        if student_number:
            student_query = """ AND student_department.student_number = '{student_number}'"""
            query += student_query.format(student_number=student_number)

        self.add_query_to_execute(query)
        return self.get_no_processing()


    def get_all_departments(self):
        query = ''' SELECT 
                        department.code,
                        department.name,
                        department.status
                    FROM department
                    WHERE department.status = TRUE'''
        self.add_query_to_execute(query)
        return self.get_no_processing()


    def get_all_departments_students(self, departments, students):
        temp = departments[:]

        for index, department in enumerate(departments, 0):
            for student in students:
                if temp[index].get('students') is None:
                    temp[index]['students'] = list()

                if student[1] == department['department_code']:
                    department_student = dict(student_number=student[0], 
                                              social_security_number=student[3], 
                                              name=student[4], 
                                              status=student[2])

                    temp[index]['students'].append(department_student)

        return temp

    
    def get_one_department_students(self, department, students):
        temp = list()

        for student in students:
            student = dict(student_number=student[0], 
                           social_security_number=student[3], 
                           name=student[4], 
                           status=student[2])
            temp.append(student)

        department['students'] = temp
        return department


    def remove_all_students(self, department_code):
        line = """  UPDATE student_department
                    SET status = FALSE
                    WHERE department_code = '{department_code}'
                    AND status = TRUE"""
        query = line.format(department_code=department_code)
        self.add_query_to_execute(query)

    
    def valid_department_exists(self, code):
        self.valid_records_exists(code, 'department', 'code')


    def get_departments_codes(self):
        query = ''' SELECT code 
                    FROM department
                    WHERE department.status = TRUE'''
        self.add_query_to_execute(query)
        return self.get_no_processing()
