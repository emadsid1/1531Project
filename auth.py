import jwt
from json import dumps #TODO get rid of
from uuid import uuid4
from exception import ValueError, AccessError
from class_defines import data, User
from helper_functions import check_email, user_from_uid

def auth_login(email, password):
    global data
    valid = False
    i = 0
    check_email(email)
    for counter, acc in enumerate(data['accounts']):
        if acc.email == email and acc.password == password:
                i = counter
                valid = True
    if (not(valid)):
        raise ValueError('email and/or password does not match any account')
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'][i].token = token.decode('utf-8')
    return dumps({'u_id': data['accounts'][i].u_id, 'token': token.decode('utf-8')})

def auth_logout(token):
    global data
    if token == '':
        return dumps({'is_success': False})
    for acc in data['accounts']:
        if token == acc.token:
            acc.token = ''
            return dumps({'is_success': True})
    return dumps({'is_success': False})

def auth_register(email, password, first, last): # TODO FIRST USER IS OWNER?
    global data

    check_email(email)

    if (len(password) <= 6): # if password is too short
        raise ValueError(description = 'Password too short') # TODO KENNY YA CUNT LOOK AT THIS

    if (not(1 <= len(first) and len(first) <= 50)): # if name is not between 1 and 50 characters long
        raise ValueError('first name must be between 1 and 50 characters long')

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
        if acc.handle.startswith(first + last): # Checking exact name repetitions
            if handle == first + last:  # If handle is base concantate case
                handle += '0'   # Add zero on end
            else:   # If NOT base case, take off number on end and add 1
                new = int(acc.handle.split(first + last)[1]) + 1
                if curr <= new: # If new number is larger replace
                    handle = first + last + str(new)
                    curr = new
        elif handle == (first + last)[:20]: # If name is truncate case and is already 20 characters
            handle += '0'
    if len(handle) > 20:    # If handle is too long make handle the hexadecimal number of account_count
        handle = hex(data['account_count'])
    user_id = data['account_count']
    data['account_count'] += 1
    handle.lower()
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'].append(User(email, password, first, last, handle, token.decode('utf-8'), user_id))
    return dumps({'u_id': user_id,'token': token.decode('utf-8')})

def reset_request(email):
    global data
    for acc in data['accounts']:
        if acc.email == email:
            resetcode = str(uuid4())
            acc.reset_code = resetcode
    return dumps({})

def reset_reset(code, password):
    global data
    for acc in data['accounts']:
        if code == acc.reset_code:
            if len(password) >= 6:
                acc.password = password
                acc.reset_code = ''
                acc.token = ''
                return dumps({})
            else:
                raise ValueError('password is too short (min length of 6)')
    raise ValueError('reset code is not valid')
