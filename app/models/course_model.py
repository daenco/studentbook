from datetime import datetime
from random import choice, randrange, randint

from faker import Faker

from app.models.model import Model

class CourseModel(Model):

    def __init__(self):
        super(CourseModel, self).__init__()

        self.columns = {
            'course.course_number': 'course_number',
            'course.offering_department': 'offering_department',
            'course.name': 'name',
            'course.description': 'description',
            'course.semester_hours': 'semester_hours',
            'course.course_level': 'course_level'
        }

        self.set_query_columns(self.columns)

    
    # department_model, str_filters=''
    def list_all(self, department_model):
        line = '''  SELECT 
                        {columns} 
                    FROM course
                    WHERE course.status = TRUE'''
        query = line.format(columns=self.get_query_columns_string())
        self.add_query_to_execute(query)
        courses = self.get_full_list()
        courses_data = courses['data']

        if len(courses_data):
            departments = department_model.get_all_departments()
            courses['data'] = self.get_all_courses_departments(courses_data, departments)

        return courses


    def get_one(self, course_number):
        line =  """ SELECT 
                        {columns} 
                    FROM course
                    WHERE course_number = '{course_number}'
                    AND course.status = TRUE"""
        query = line.format(columns=self.get_query_columns_string(),
                            course_number=course_number)
        self.add_query_to_execute(query)

        return self.get_one_row()
        # student_data = student['data']

        # if len(student_data):
        #     departments = department_model.get_departments(student_number)
        #     student['data'] = self.get_one_student_departments(student_data, 
        #                                                        departments)

        # return student


    # department_code=None,
    def save_one(self, data_fields, department_code, **kwargs):
        course_number = self.get_index(kwargs.get('course_number'))
        self.valid_department_exists(department_code)
        self.set_queries_to_save(course_number, department_code, data_fields)

        # if department_code:
        #     self.valid_records_exists(department_code, 'department', 'code')
        #     self.add_to_department(student_number, department_code)
            
        return self.execute_query()


    def set_queries_to_save(self, course_number, department_code, data_fields):
        line = """  INSERT INTO course
                    VALUES (
                        {course_number},
                        {offering_department},
                        '{name}',
                        '{description}',
                        {semester_hours},
                        {course_level}
                    )"""
        query = line.format(course_number=course_number, 
                            offering_department=department_code, 
                            **data_fields)
        self.add_query_to_execute(query)


    # department_model
    def save_faked_courses(self, num_courses, department_code):
        fake = Faker()

        # departments = department_model.get_departments_codes()

        for _ in range(0, num_courses):
            course_number = self.get_uuid()

            data_fields = {
                'name': fake.job(),
                'description': fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                'semester_hours': randrange(70, 120, 10),
                'course_level': randint(1, 10)
            }

            self.set_queries_to_save(course_number, department_code, data_fields)
            # self.add_to_department(student_number, choice(departments)[0])

        return self.execute_queries()

 
    # def modify_one(self, data_fields, student_number, current_department=None,
    #                new_department=None):
    #     self.valid_student_exists(student_number)

    #     line = """  UPDATE student
    #                 SET social_security_number = {social_security_number},
    #                     first_name = '{first_name}',
    #                     last_name = '{last_name}',
    #                     date_of_birth = '{date_of_birth}',
    #                     sex = '{sex}',
    #                     current_address = '{current_address}',
    #                     current_phone_number = '{current_phone_number}',
    #                     permanent_address = '{permanent_address}',
    #                     permanent_phone_number = '{permanent_phone_number}',
    #                     class = '{class}'
    #                 WHERE student_number = '{student_number}'
    #                 AND status = TRUE"""
    #     query = line.format(student_number=student_number, **data_fields)
    #     self.add_query_to_execute(query)

    #     if current_department and new_department:
    #         self.valid_department_exists(current_department)
    #         self.valid_department_exists(new_department)

    #         self.change_department(student_number, current_department, 
    #                                new_department)
    #         return self.execute_queries()

    #     return self.execute_query()


    # def delete_one(self, student_number):
    #     self.valid_student_exists(student_number)

    #     line = """UPDATE student 
    #               SET status = FALSE 
    #               WHERE student_number = '{student_number}'
    #               AND status = TRUE"""
    #     query = line.format(student_number=student_number)
    #     self.add_query_to_execute(query)
    #     self.remove_from_departments(student_number)

    #     return self.execute_queries()


    def clear_course_table(self):
        tables = [
            'course'
        ]

        for table in tables:
            query = "DELETE FROM {table}".format(table=table)
            self.add_query_to_execute(query)

        return self.execute_queries()


    # def valid_student_exists(self, number):
    #     self.valid_records_exists(number, 'student', 'student_number')

    
    def valid_department_exists(self, code):
        self.valid_records_exists(code, 'department', 'code')


    # def get_students(self, department_code=None):
    #     query = ''' SELECT 
    #                     student_department.student_number,
    #                     student_department.department_code,
    #                     student_department.status,
    #                     student.social_security_number,
    #                     student.first_name,
    #                     student.last_name
    #                 FROM student
    #                 JOIN student_department ON student.student_number = student_department.student_number
    #                 WHERE student.status = TRUE
    #                 AND student_department.status = TRUE'''

    #     if department_code:
    #         department_query = """ AND student_department.department_code = '{department_code}'"""
    #         query += department_query.format(department_code=department_code)

    #     self.add_query_to_execute(query)
    #     return self.get_no_processing()

    
    def get_all_courses_departments(self, courses, departments):
        temp = courses[:]

        for index, course in enumerate(courses, 0):
            for department in departments:
                if temp[index].get('departments') is None:
                    temp[index]['departments'] = list()

                if department[0] == course['offering_department']:
                    course_department = dict(department_code=department[0], 
                                             name=department[1],
                                             status=department[2])

                    temp[index]['departments'].append(course_department)

        return temp

    
    # def get_one_student_departments(self, student, departments):
    #     temp = list()

    #     for department in departments:
    #         department = dict(department_code=department[1], 
    #                           first_name=department[3], 
    #                           last_name=department[4], 
    #                           status=department[2])
    #         temp.append(department)

    #     student['departments'] = temp
    #     return student


    # def add_to_department(self, student_number, department_code):
    #     line = """  INSERT INTO student_department
    #                 (student_number, department_code, 
    #                 from_start_date)
    #                 VALUES (
    #                     '{student_number}',
    #                     '{department_code}',
    #                     '{from_start_date}'
    #                 )"""
    #     query = line.format(student_number=student_number, 
    #                         department_code=department_code,
    #                         from_start_date=datetime.now().date())
    #     self.add_query_to_execute(query)


    # def change_department(self, student_number, current_department, 
    #                       new_department):
    #     line = """  UPDATE student_department
    #                 SET status = FALSE,
    #                     until_end_date = '{until_end_date}'
    #                 WHERE student_number = '{student_number}'
    #                 AND department_code = '{current_department}'
    #                 AND status = TRUE"""
    #     query = line.format(until_end_date=datetime.now().date(), 
    #                         student_number=student_number, 
    #                         current_department=current_department)
    #     self.add_query_to_execute(query)
        # self.add_to_department(student_number, new_department)


    # def remove_from_departments(self, student_number):
    #     line = """  UPDATE student_department
    #                 SET status = FALSE
    #                 WHERE student_number = '{student_number}'
    #                 AND status = TRUE"""
    #     query = line.format(student_number=student_number)
    #     self.add_query_to_execute(query)
