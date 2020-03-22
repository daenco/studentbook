from datetime import datetime
from random import choice

from faker import Faker

from app.models.model import Model

class StudentModel(Model):

    def __init__(self):
        super(StudentModel, self).__init__()

        self.columns = {
            'student.student_number': 'student_number',
            'student.social_security_number': 'social_security_number',
            'student.first_name': 'first_name',
            'student.last_name': 'last_name',
            'student.date_of_birth::text': 'date_of_birth',
            'student.sex': 'sex',
            'student.current_address': 'current_address',
            'student.current_phone_number': 'current_phone_number',
            'student.permanent_address': 'permanent_address',
            'student.permanent_phone_number': 'permanent_phone_number',
            'student.class': 'class',
            'permanent_address_detail.city': 'city',
            'permanent_address_detail.state': 'state',
            'permanent_address_detail.zip_code': 'zip_code'
        }

        self.set_query_columns(self.columns)

    
    def list_all(self, department_model, str_filters=''):
        line = '''  SELECT 
                        {columns} 
                    FROM student
                    LEFT JOIN permanent_address_detail USING(student_number)
                    WHERE student.status = TRUE {str_filters}'''
        query = line.format(columns=self.get_query_columns_string(),
                            str_filters=str_filters)
        self.add_query_to_execute(query)
        students = self.get_full_list()
        students_data = students['data']

        if len(students_data):
            departments = department_model.get_departments()
            students['data'] = self.get_all_students_departments(students_data, departments)

        return students


    def get_one(self, student_number, department_model):
        line =  """ SELECT 
                        {columns} 
                    FROM student
                    LEFT JOIN permanent_address_detail USING(student_number)
                    WHERE student_number = '{student_number}'
                    AND student.status = TRUE"""
        query = line.format(columns=self.get_query_columns_string(),
                            student_number=student_number)
        self.add_query_to_execute(query)

        student = self.get_one_row()
        student_data = student['data']

        if len(student_data):
            departments = department_model.get_departments(student_number)
            student['data'] = self.get_one_student_departments(student_data, 
                                                               departments)

        return student


    def set_queries_to_save(self, student_number, data_fields):
        line = """  INSERT INTO student
                    VALUES (
                        '{student_number}',
                        '{social_security_number}',
                        '{first_name}',
                        '{last_name}',
                        '{date_of_birth}',
                        '{sex}',
                        '{current_address}',
                        '{current_phone_number}',
                        '{permanent_address}',
                        '{permanent_phone_number}',
                        '{class}'
                    )"""
        query = line.format(student_number=student_number, **data_fields)
        self.add_query_to_execute(query)

        line = """  INSERT INTO permanent_address_detail
                    VALUES (
                        '{student_number}',
                        '{city}',
                        '{state}',
                        '{zip_code}'
                    )"""
        query = line.format(student_number=student_number, **data_fields)
        self.add_query_to_execute(query)


    def save_one(self, data_fields, department_code=None, **kwargs):
        student_number = self.get_index(kwargs.get('student_number'))

        self.set_queries_to_save(student_number, data_fields)

        if department_code:
            self.valid_records_exists(department_code, 'department', 'code')
            self.add_to_department(student_number, department_code)
            
        return self.execute_queries()

    
    def save_faked_students(self, num_students, department_model):
        fake = Faker()

        departments = department_model.get_departments_codes()

        for _ in range(0, num_students):
            student_number = self.get_uuid()

            data_fields = {
                'social_security_number': fake.itin(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'date_of_birth': fake.date(pattern="%Y-%m-%d", end_datetime=None),
                'sex': choice(['M', 'F']),
                'current_address': fake.address(),
                'current_phone_number': fake.phone_number(),
                'permanent_address': fake.address(),
                'permanent_phone_number': fake.phone_number(),
                'class': fake.job(),
                'city': fake.city(),
                'state': fake.state(),
                'zip_code': fake.zipcode()
            }

            self.set_queries_to_save(student_number, data_fields)

            self.add_to_department(student_number, choice(departments)[0])

        return self.execute_queries()

 
    def modify_one(self, data_fields, student_number, current_department=None,
                   new_department=None):
        self.valid_student_exists(student_number)

        line = """  UPDATE student
                    SET social_security_number = {social_security_number},
                        first_name = '{first_name}',
                        last_name = '{last_name}',
                        date_of_birth = '{date_of_birth}',
                        sex = '{sex}',
                        current_address = '{current_address}',
                        current_phone_number = '{current_phone_number}',
                        permanent_address = '{permanent_address}',
                        permanent_phone_number = '{permanent_phone_number}',
                        class = '{class}'
                    WHERE student_number = '{student_number}'
                    AND status = TRUE"""
        query = line.format(student_number=student_number, **data_fields)
        self.add_query_to_execute(query)

        if current_department and new_department:
            self.valid_department_exists(current_department)
            self.valid_department_exists(new_department)

            self.change_department(student_number, current_department, 
                                   new_department)
            return self.execute_queries()

        return self.execute_query()


    def delete_one(self, student_number):
        self.valid_student_exists(student_number)

        line = """UPDATE student 
                  SET status = FALSE 
                  WHERE student_number = '{student_number}'
                  AND status = TRUE"""
        query = line.format(student_number=student_number)
        self.add_query_to_execute(query)
        self.remove_from_departments(student_number)

        return self.execute_queries()


    def clear_student_table(self):
        tables = [
            'student_department', 
            'permanent_address_detail', 
            'student'
        ]

        for table in tables:
            query = "DELETE FROM {table}".format(table=table)
            self.add_query_to_execute(query)

        return self.execute_queries()


    def valid_student_exists(self, number):
        self.valid_records_exists(number, 'student', 'student_number')

    
    def valid_department_exists(self, code):
        self.valid_records_exists(code, 'department', 'code')


    def get_students(self, department_code=None):
        query = ''' SELECT 
                        student_department.student_number,
                        student_department.department_code,
                        student_department.status,
                        student.social_security_number,
                        student.first_name,
                        student.last_name
                    FROM student
                    JOIN student_department ON student.student_number = student_department.student_number
                    WHERE student.status = TRUE
                    AND student_department.status = TRUE'''

        if department_code:
            department_query = """ AND student_department.department_code = '{department_code}'"""
            query += department_query.format(department_code=department_code)

        self.add_query_to_execute(query)
        return self.get_no_processing()

    
    def get_all_students_departments(self, students, departments):
        temp = students[:]

        for index, student in enumerate(students, 0):
            for department in departments:
                if temp[index].get('departments') is None:
                    temp[index]['departments'] = list()

                if department[0] == student['student_number']:
                    student_department = dict(department_code=department[1], 
                                              name=department[3],
                                              status=department[2])

                    temp[index]['departments'].append(student_department)

        return temp

    
    def get_one_student_departments(self, student, departments):
        temp = list()

        for department in departments:
            department = dict(department_code=department[1], 
                              first_name=department[3], 
                              last_name=department[4], 
                              status=department[2])
            temp.append(department)

        student['departments'] = temp
        return student


    def add_to_department(self, student_number, department_code):
        line = """  INSERT INTO student_department
                    (student_number, department_code, 
                    from_start_date)
                    VALUES (
                        '{student_number}',
                        '{department_code}',
                        '{from_start_date}'
                    )"""
        query = line.format(student_number=student_number, 
                            department_code=department_code,
                            from_start_date=datetime.now().date())
        self.add_query_to_execute(query)


    def change_department(self, student_number, current_department, 
                          new_department):
        line = """  UPDATE student_department
                    SET status = FALSE,
                        until_end_date = '{until_end_date}'
                    WHERE student_number = '{student_number}'
                    AND department_code = '{current_department}'
                    AND status = TRUE"""
        query = line.format(until_end_date=datetime.now().date(), 
                            student_number=student_number, 
                            current_department=current_department)
        self.add_query_to_execute(query)
        self.add_to_department(student_number, new_department)


    def remove_from_departments(self, student_number):
        line = """  UPDATE student_department
                    SET status = FALSE
                    WHERE student_number = '{student_number}'
                    AND status = TRUE"""
        query = line.format(student_number=student_number)
        self.add_query_to_execute(query)
