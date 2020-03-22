from flask_restful import abort

def show_abort(http_code=400, data={ 'message': 'Error no defined.' }):
    abort(http_code, **data)