from collections import defaultdict
from datetime import datetime

from flask import request

from app.sys_utils.errors import show_abort

class Controller(object):

    def __init__(self):
        self.request_info = {
            'method': request.method,
            'path': request.path,
            'url_args': request.args,
            'result': {}
        }

        self.url_args = request.args

        self.data_inputs = defaultdict(None)

        self.data_fields = defaultdict(None)

        self.filters = defaultdict(None)


    def valid_required_arg(self, arg):
        if self.url_args.get(arg) is None:
            message = "The field '{arg}' is required."
            show_abort(data={ 'message': message.format(arg=arg) })

    
    def get_header_sent(self):
        return request.headers.get('Content-Type', None)

        
    def get_data_input(self, required_fields):
        headers_allowed = ['application/x-www-form-urlencoded', 'application/json']
        header = self.get_header_sent()

        if header not in headers_allowed:
            message = 'Only headers allowed: {}'
            show_abort(data={ 'message': message.format(', '.join(headers_allowed)) })

        if header == headers_allowed[0]:
            self.data_inputs = request.form

            if self.data_inputs != required_fields:
                show_abort(data={ 'message': 'We could not get data correctly.' })
        elif request.is_json:
            try:
                self.data_inputs = request.json
            except:
                show_abort(data={ 'message': 'Data must be in JSON format.' })
        
    
    def valid_data_fields(self):
        missing_fields = [key for key, value in self.data_fields.items() if value is None]

        if len(missing_fields):
            message = 'The following fields are required: {}'
            show_abort(data={ 'message': message.format(', '.join(missing_fields)) })


    def get_fields_input(self, required_fields={}):
        self.get_data_input(required_fields)

        for field, to_get in required_fields.items():
            self.data_fields[field] = to_get(field, self.data_inputs)

        self.valid_data_fields()


    def get_date(self, value):
        try:
            return datetime.strptime(value.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None


    def get_integer(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None


    def set_filters(self, filters):
        for _filter in filters:
            self.filters[_filter] = None


    def set_query_filters(self):
        for _filter in self.filters.keys():
            value = self.url_args.get(_filter)

            if _filter == 'min_date' or _filter == 'max_date':
                value = self.get_date(str(value))
            elif _filter == 'limit':
                value = self.get_integer(value)
            
            self.filters[_filter] = value


    def get_query_filters(self, filters=[]):
        str_filters = ""

        self.set_filters(filters)
        self.set_query_filters()

        if self.filters['min_date'] and self.filters['max_date']:
            str_filters = " AND date_of_birth BETWEEN '{min_date}' AND '{max_date}'"
        elif self.filters['min_date']:
            str_filters = " AND date_of_birth >= '{min_date}'"
        elif self.filters['max_date']:
            str_filters = " AND date_of_birth <= '{max_date}'"

        if self.filters['name']:
            str_filters += self.check_str_query_filter(str_filters)
            str_filters += " first_name LIKE '%{name}%' OR last_name LIKE '%{name}%' "

        if self.filters['limit']:
            str_filters += " LIMIT {limit}"
        
        return str_filters.format(**self.filters)

    
    def get_url_arg(self, arg):
        return self.url_args.get(arg)


    def check_str_query_filter(self, str_filters):
        return ' AND' if len(str_filters) else ''