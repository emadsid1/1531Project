from flask import Flask, request
from json import dumps
from uuid import uuid4
from class_defines import data, user, channel, mesg, reacts, account_count
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
        raise ValueError('email and/or password does not match any account')
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'][i].token = token.decode('utf-8')
    return dumps({'u_id': data['accounts'][i].user_id, 'token': token.decode('utf-8')})

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
    global account_count

    email = request.form.get('email')
    check_email(email)

    password = request.form.get('password')
    if (len(password) < 6): # if password is too short
        raise ValueError('password is too short (min length of 6)')

    first = request.form.get('name_first')
    if (not(1 <= len(first) and len(first) <= 50)): # if name is not between 1 and 50 characters long
        raise ValueError('first name must be between 1 and 50 characters long')

    last = request.form.get('name_last')
    if (not(1 <= len(last) and len(last) <= 50)):   # if name is not between 1 and 50 characters long
        raise ValueError('last name must be between 1 and 50 characters long')

    handle = first + last
    if len(handle) > 20:
        handle = handle[:20]
    curr = 0
    new = 0
    for acc in data['accounts']:
        if acc.email == email:  # if email is already registered
            raise ValueError('email already matches an existing account')
        if acc.handle.startswith(first + last): # confirm handle is unique
            if handle == first + last:
                handle += '0'
            else:
                new = int(acc.handle.split(first + last)[1]) + 1
                if curr <= new:
                    handle = first + last + str(new)
                    curr = new
        elif handle == (first + last)[:20]:
            handle += '0'
    if len(handle) > 20:
        handle = hex(account_count)
        account_count += 1
    handle.lower()
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    user_id = str(uuid4())
    data['accounts'].append(user(email, password, first, last, handle, token.decode('utf-8'), user_id))
    return dumps({'u_id': user_id,'token': token.decode('utf-8')})

@app.route('/auth/passwordreset/request', methods = ['POST'])
def reset_request():
    email = request.form.get('email')
    for acc in data['accounts']:
        if acc.email == email:
            # TODO SEND EMAIL
            acc.reset_code = 'RESETCODE'
            return dumps({})
    return dumps({})

@app.route('/auth/passwordreset/reset', methods = ['POST'])
def reset_reset():
    code = request.form.get('reset_code')
    password = request.form.get('new_password')
    for acc in data['accounts']:
        if code == acc.reset_code:
            if len(password) >= 6:
                acc.password = password
                acc.reset_code = ''
                acc.token = ''
                return dumps({})
            else:
                raise ValueError('password is too short (min length of 6)')
    raise ValueError('reset code is invalid')
    pass

# Helpers
def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not(re.search(regex,email))):    # if not valid email
        raise ValueError('not a valid email')

# Run flask
if __name__ == '__main__':
    app.run(debug=True)

# TODO email sending, check assumptions (when to login when to logout etc)
