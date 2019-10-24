from flask import Flask, request
from json import dumps
from class_defines import data, user, channel, mesg, reacts
import re
import jwt

app = Flask(__name__)
# Echo functions
@app.route('/echo/post', methods = ['POST'])
def echo_post():
    echo_input = request.form.get('echo')
    return dumps({'echo': echo_input})

@app.route('/echo/get', methods = ['GET'])
def echo_get():
    echo_input = requets.args.get('echo')
    return dumps({'echo': echo_input})

# Echo functions
@app.route('/auth/login', methods = ['POST'])
def auth_login():
    global data
    valid = False
    i = 0
    email = request.form.get('email')
    check_email(email)
    password = request.form.get('password')
    for counter, acc in enumerate(data['accounts']):
        if acc.email == email and acc.password == password:
                i = counter
                valid = True
    if (not(valid)):
        raise Exception('ValueError')
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'][i].token = token.decode('utf-8')
    return dumps({'u_id': 12345, 'token': token.decode('utf-8')})

@app.route('/auth/logout', methods = ['POST'])
def auth_logout():
    token = request.form.get('token')
    if token == '':
        return dumps({'is_success': False})
    for acc in data['accounts']:
        if token == acc.token:
            acc.token = ''
            return dumps({'is_success': True})
    return dumps({'is_success': False})

@app.route('/auth/register', methods = ['POST'])
def auth_register():
    global data

    email = request.form.get('email')
    check_email(email)

    password = request.form.get('password')
    if (len(password) < 6): # if password is too short
        raise Exception('ValueError')
<<<<<<< HEAD

=======

>>>>>>> COMP1531/19T3-cs1531-project-master
    first = request.form.get('name_first')
    if (not(1 <= len(first) and len(first) <= 50)): # if name is not between 1 and 50 characters long
        raise Exception('ValueError')

    last = request.form.get('name_last')
    if (not(1 <= len(last) and len(last) <= 50)):   # if name is not between 1 and 50 characters long
        raise Exception('ValueError')

    handle = first + last
    curr = 0
    new = 0
    for acc in data['accounts']:
        if acc.email == email:  # if email is already register
            raise Exception('ValueError')
        if acc.handle.startswith(first + last): # confirm handle is unique
            if handle == first + last:
                handle += '0'
            else:
                new = int(acc.handle.split(first + last)[1]) + 1
                if curr <= new:
                    handle = first + last + str(new)
                    curr = new
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'].append(user(email, password, first, last, handle, token.decode('utf-8')))
    return dumps({'token': token.decode('utf-8')})

@app.route('/auth/passwordreset/request', methods = ['POST'])
def reset_request():
    email = request.form.get('email')
    for acc in data['accounts']:
        if acc.email == email:
            # TODO SEND EMAIL
            return dumps({})
    return dumps({})

@app.route('/auth/passwordreset/reset', methods = ['POST'])
def reset_reset():
    pass

# Helpers
def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not(re.search(regex,email))):    # if not valid email
<<<<<<< HEAD
        raise Exception('ValueError')

# Run flask
if __name__ == '__main__':
    app.run(debug=True)
=======
        raise Exception('ValueError')

# Run flask
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> COMP1531/19T3-cs1531-project-master
