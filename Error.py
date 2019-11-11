# """

# 1) Run the flask server
# 2) Access /valueerror

# Note: You may need to run "pip3 install flask_cors" for this to work

# Would strongly recommend using this pattern for iteration 2

# A lot of this code isn't meant to be fully explained by us - but you're
#  welcome to do your own reading to make sense of it. The gist of it is that
#  you can register an error handler, that is a function, and tell flask
#  to call that function every time an exception of a certain type is thrown.
#  What this code is saying to flask is "Every time you have an Exception
#  thrown please call this particular function. In this case, our function is
#   "defaultHandler" which just takes in an error type and packages it up
#  to be sent to the frontend
# """

# from flask import Flask, request, jsonify
# from werkzeug.exceptions import HTTPException
# from flask_cors import CORS
# from json import dumps

# def defaultHandler(err):
#     response = err.get_response()
#     response.data = dumps({
#         "code": err.code,
#         "name": "System Error",
#         "message": err.description,
#     })
#     response.content_type = 'application/json'
#     return response

# app = Flask(__name__)
# app.config['TRAP_HTTP_EXCEPTIONS'] = True
# app.register_error_handler(Exception, defaultHandler)
# CORS(app)

# class ValueError(HTTPException):
#     code = 400
#     message = 'No message specified'

# # Post
# @app.route('/valueerror')
# def login():
#     raise ValueError(description="Channel name is bad")

# if __name__ == '__main__':
#     app.run(debug=True)
