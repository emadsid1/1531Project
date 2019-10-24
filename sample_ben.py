"""Flask server from M13A-SNAKE"""
from json import dumps
from flask import Flask, request
from class_defines import data, user, channel, mesg, reacts
from datetime import datetime, timedelta
from Error import AccessError
import re

app = Flask(__name__)

@app.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@app.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })


@app.route('/user/profile', methods=['GET'])
def user_profile():
    global data
    token = request.args.get("token")
    valid = False
    user = {}
    for acc in data["accounts"]:
        if token == acc.token: # note: assumes token is valid
            if request.args.get("u_id") == acc.user_id:
                valid = True
            else:
                raise Exception("ValueError")
    if valid == True:
        user["email"] = acc.email
        user["name_first"] == acc.name_first
        user["name_last"] == acc.name_last
        user["handle_str"] == acc.handle
    return dumps({
    "email": user["email"],
    "name_first": user["name_first"],
    "name_last": user["name_last"],
    "handle_str": user["handle_str"]
    })

@app.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    global data
    token = request.form.get("token") #assume token is valid

    name_first = request.form.get("name_first")
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise Exception("ValueError")

    name_last = request.form.get("name_last")
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise Exception("ValueError")

    for acc in data["accounts"]:
        if token == acc.token:
            acc.name_first == name_first
            acc.name_last == name_last

    return dumps({})


@app.route('/user/profile/setemail', methods=['PUT'])
def user_profile_email():
    global data
    token = request.form.get("token") # assume token is valid
    email = request.form.get("email")
    check_email(email)
    number = None
    for acc in data["accounts"]:
        if token == acc.token:
            number = acc
        if email == acc.email:
            raise Exception("ValueError")
    if number is not None:
        data["accounts"][number].email = email
    return dumps({})

@app.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    global data
    token = request.form.get("token") # assume token is valid
    handle = request.form.get("handle_str")
    if len(handle) < 3 or len(handle) > 20:
        raise Exception("ValueError")
    number = None
    for acc in data["accounts"]:
        if token == acc.token:
            number = acc
        if handle == acc.handle:
            raise Exception("ValueError")
    if number is not None:
        data["accounts"][number].handle = handle
    return dumps({})

@app.route('/user/profiles/uploadphoto', methods=['POST'])
# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def user_profile_uploadphoto():
    request = request.get("img_url")
    if request != 200:
        raise Exception("ValueError")
    url = request.form.get("img_url")
    # how to get image size?
    return dumps({})

@app.route('/standup/start', methods=['POST'])
def standup_start():
    token = request.form.get("token") #assume token is valid
    channel = request.form.get("channel_id")
    valid = False
    in_channel = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            valid = True
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise Exception("ValueError") # channel does not exist

    for acc in data["channels"][ch_counter].owners: # search owners list
        if token == acc.token:
            in_channel = True
    if in_channel == False:
        for acc in data["channels"][ch_counter].admins: # search admins list
            if token == acc.token:
                in_channel = True
    if in_channel == False:
        for acc in data["channels"][ch_counter].members: # search members list
            if token == acc.token:
                in_channel = True
    if in_channel == False: # if the user is not in the channel, raise an error
        raise Exception("AccessError") # need to write this function

    data["channels"][ch_counter].is_standup = True
    data["channels"][ch_counter].standup_time = datetime.now()
    standup_finish = data["channels"][ch_counter].standup_time + timedelta(minutes=15)

    return dumps({standup_finish})

@app.route('/standup/send', methods=['POST'])
def standup_send():
    token = request.form.get("token") # assume token is valid
    channel = request.form.get("channel_id")
    valid = False
    in_channel = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            if ch.is_standup == False:
                raise Exception("ValueError") # standup is not happening atm
            valid = True
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise Exception("ValueError") # channel does not exist

    message = request.form.get("message")
    if len(message) > 1000:
        raise Exception("ValueError") # message too long

    for acc in data["channels"][ch_counter].owners: # search owners list
        if token == acc.token:
            in_channel = True
    if in_channel == False:
        for acc in data["channels"][ch_counter].admins: # search admins list
            if token == acc.token:
                in_channel = True
    if in_channel == False:
        for acc in data["channels"][ch_counter].members: # search members list
            if token == acc.token:
                in_channel = True
    if in_channel == False: # if the user is not in the channel, raise an error
        raise Exception("AccessError") # need to write this function

    # TODO: how to check if standup has finished?
    data["channels"][ch_counter].standup_messages.append(message)
    return dumps({})

@app.route('/search', methods=['GET'])
def search():
    token = request.args.get("token")
    for acc in data["accounts"]:
        if token == acc.token:
            ch_list = acc.in_channel
    query_str = request.args.get("query_str")
    messages = []
    for ch in ch_list: # assume in_channel object is list of channel classes
        for msg in ch.messages:
            if query_str in msg.message:
                messages.append({
                    "message_id": msg.message_id,
                    "u_id": msg.sender.user_id,
                    "message": msg.message,
                    "time_created": msg.create_time,
                    "reacts": msg.reaction,
                    "is_pinned": msg.pin
                })

    return dumps({messages})

@app.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission_change():
    perm_id = request.form.get("permission_id")
    if perm_id < 1 or perm_id > 3:
        raise Exception("ValueError") # invalid perm_id
    user_id = request.form.get("u_id")
    valid = False
    token = request.form.get("token") # assume token is valid
    for acc in data["accounts"]:
        if token == acc.token:
            if acc.permission_id == 3:
                raise Exception("AccessError") # members do not have permission to change perm_id
        if user_id == acc.user_id:
            valid = True
    if valid == False:
        raise Exception("ValueError") # user does not exist
    return dumps({})

# Helper functions
def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not(re.search(regex,email))):    # if not valid email
        raise Exception('ValueError')

if __name__ == '__main__':
    app.run(debug=True)
