from werkzeug.exceptions import HTTPException

class ValueError(HTTPException):
    code = 400
    message = 'No message specified'

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'