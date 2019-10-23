from flask import Flask, request
from json import dumps
import re 
import jwt
import class_defines.py

app = Flask(__name__)

@app.route('/echo/post', methods = ['POST'])
def echo_post():
    echo_input = request.form.get('echo')
    return dumps({'echo': echo_input})

@app.route('/echo/get', methods = ['GET'])
def echo_get():
    echo_input = requets.args.get('echo')
    return dumps({'echo': echo_input})

@app.route('/auth/register', methods = ['POST'])
def auth_register():
    global users
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    email = request.form.get('email')
    if(not (re.search(regex,email))):
        raise Exception('ValueError')
    for acc in accounts:
        if acc.email == email:
            raise Exception('ValueError')
    password = request.form.get('password')
    if (len(password) < 6):
        raise Exception('ValueError')
    first = request.form.get('name_first')
    if (not(1 <= len(first) and len(first) <= 50)):
        raise Exception('ValueError')
    last = request.form.get('name_last')
    if (not(1 <= len(last) and len(last) <= 50)):
        raise Exception('ValueError')
    new_user = user(email, password, first, last)
    accounts.append(new_user)
    token = jwt.encode({'email': email, 'password': password}, 'this is a secret secret :o',algorithm = 'HS256')
    return dumps({'token': token.decode('utf-8')})
    

if __name__ == '__main__':
    app.run(debug=True)