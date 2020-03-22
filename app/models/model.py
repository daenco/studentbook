import logging
from uuid import uuid1

from flask_restful import abort
from psycopg2 import Error

from app.sys_utils.pg_connection import PGConnection

messages = {
    200: 'OK',
    404: 'Record not found',
    501: 'The request could not be proccesed',
    503: 'The MySQL server does not respond, please try to start as a service',
}

class Model(object):

    def __init__(self):
        try:
            self.connection = PGConnection()
        except Exception as error:
            abort(503, **{ 'message': messages[503] })

        self.set_default_query_info()

        self.queries = None


    def get_full_list(self):
        try:
            data = self.map_data_queried(self.connection.execute_get())
            self.query_info['data'] = data
            self.query_info['affected_rows'] = len(data) 
        except Error:
            self.query_info['status'] = 501
            self.query_info['message'] = messages[501]
            logging.exception(messages[501])

        return self.query_info


    def get_one_row(self):
        try:
            data = self.map_row_queried(self.connection.execute_get(one_row=True))

            if data:
                self.query_info['data'] = data
                self.query_info['affected_rows'] = len([data]) 
            else:
                self.query_info['status'] = 404 
                self.query_info['message'] = messages[404]
        except Error:
            self.query_info['status'] = 501
            self.query_info['message'] = messages[501]
            logging.exception(messages[501])

        return self.query_info

    
    def get_no_processing(self, one_row=False):
        return self.connection.execute_get(one_row)

    
    def execute_query(self):
        try:
            self.query_info['affected_rows'] = self.connection.execute_one_query()
        except Error:
            self.query_info['status'] = 501
            self.query_info['message'] = messages[501]
            logging.exception(messages[501])

        return self.query_info


    def execute_queries(self):
        try:
            self.query_info['affected_rows'] = self.connection.execute_many_queries()
        except Error:
            self.query_info['status'] = 501
            self.query_info['message'] = messages[501]
            logging.exception(messages[501])

        return self.query_info


    def valid_records_exists(self, id_record, db_table, pk_table):
        self.hold_queries_to_execute()

        line = """  SELECT * FROM {db_table}
                    WHERE {pk_table} = '{id_record}'
                    AND status = TRUE"""
        query = line.format(db_table=db_table, pk_table=pk_table, id_record=id_record)
        self.add_query_to_execute(query)

        if self.get_no_processing(one_row=True):
            self.load_back_queries_to_execute()
            return True

        abort(404, **{ 'message': "The '{id_record}' does not exist in the '{db_table}' table.".format(
            id_record=id_record, db_table=db_table) })


    def valid_record_no_exists(self):
        record = self.get_no_processing()
        return True if len(record) == 0 else False

    
    def set_default_query_info(self):
        self.query_info = {
            'message': messages[200],
            'status': 200,
            'affected_rows': 0,
            'data': {}
        }


    def add_query_to_execute(self, query):
        self.connection.queries_list.append(query)


    def hold_queries_to_execute(self):
        self.queries = self.connection.queries_list[:]
        self.connection.queries_list.clear()


    def load_back_queries_to_execute(self):
        self.connection.queries_list.clear()
        self.connection.queries_list.extend(self.queries)

    
    def set_query_columns(self, columns):
        self.columns = columns


    def get_query_columns_string(self):
        return ', '.join(self.columns.keys())


    def get_uuid(self):
        return uuid1().time_low

    
    def get_index(self, sent_value):
        return self.get_uuid() if not sent_value else sent_value


    def map_data_queried(self, queried_data):
        columns_to_map = list(self.columns.values())
        temp_row = dict()
        mapped_data = list()

        for row in queried_data:
            for index, column in enumerate(row):
                key = columns_to_map[index]
                temp_row[key] = column
            mapped_data.append(temp_row)
            temp_row = {}
        
        return mapped_data


    def map_row_queried(self, queried_row):
        if not queried_row: 
            return dict()

        columns_to_map = list(self.columns.values())
        mapped_row = dict()

        for index, column in enumerate(queried_row):
            key = columns_to_map[index]
            mapped_row[key] = column

        return mapped_row
