from datetime import datetime

from app.sys_utils.errors import show_abort

def to_string(field, data_inputs):
    return str(data_inputs.get(field))


def to_integer(field, data_inputs):
    try:
        return int(data_inputs.get(field))
    except ValueError:
        show_abort(data={ 'message': "The field '{field}' must be an integer".format(field=field) })


def to_date(field, data_inputs):
    try:
        return datetime.strptime(data_inputs.get(field), '%Y-%m-%d')
    except ValueError:
        show_abort(data={ 'message': "The field '{field}' must be a date".format(field=field) })


def valid_index(value):
    if value is None or len(value) == 0: 
        return None
    else:
        return parse_index_to_integer(value)


def parse_index_to_integer(value):
    try:
        return int(value)
    except ValueError:
        show_abort(data={ 'message': "The record index must be an integer".format(value=value) })
