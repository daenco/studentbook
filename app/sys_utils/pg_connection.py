import logging

from psycopg2 import connect, Error

class PGConnection(object):

    def __init__(self):
        self.queries_list = []

        try:
            self.connect = connect(
                user='postgres',
                password='123456',
                host='127.0.0.1', 
                port='5432', 
                database='studentbook')

            logging.info('Database connection created.')
            self.cursor = self.connect.cursor()
        except (Exception, Error) as error:
            logging.exception(error)

    
    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
            logging.info('Database connection closed.')
        except Exception as error:
            logging.exception(error)

    
    def execute_one_query(self):
        try:
            self.cursor.execute(self.queries_list[0])
            self.connect.commit()
            logging.debug(self.cursor.query)
            return self.cursor.rowcount
        except Error as error:
            self.connect.rollback()
            logging.exception(error)
            raise Error(error)
        finally:
            self.queries_list.clear()

    
    def execute_many_queries(self):
        affected_ones = dict()

        try:
            for k, query in enumerate(self.queries_list, 1):
                self.cursor.execute(query)
                affected_ones[k] = self.cursor.statusmessage
                logging.debug(self.cursor.query)
            self.connect.commit()
            return affected_ones
        except Error as error:
            self.connect.rollback()
            logging.exception(error)
            raise Error(error)
        finally:
            self.queries_list.clear()

    
    def execute_get(self, one_row=False):
        try:
            self.cursor.execute(self.queries_list[0])
            logging.debug(self.cursor.query)
            return self.cursor.fetchall() if not one_row else self.cursor.fetchone()
        except Error as error:
            logging.exception(error)
            raise Error(error)
        finally:
            self.queries_list.clear()
