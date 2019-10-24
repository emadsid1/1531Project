"""Flask server from M13A-SNAKE"""
from json import dumps
from flask import Flask, request
from class_defines import data, user, channel, mesg, reacts
from datetime import datetime, timedelta
import AccessError

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
        if token == acc.token: #note: assumes token is valid
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
    token = request.form.get("token") #assume token is valid
    email = request.form.get("email")
    #if email is invalid, raise ValueError
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
    token = request.form.get("token") #assume token is valid
    handle = request.form.get("handle_str")
    if len(handle) < 3 or len(handle) > 20:
        raise Exception("ValueError")
    #if email is invalid, raise ValueError
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
def user_profile_uploadphoto():
    request = request.get("img_url")
    if request != 200:
        raise Exception("ValueError")
    url = request.form.get("img_url")
    #how to get image size?
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
    message = request.form.get("message")
    valid = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            valid = True
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise Exception("ValueError") # channel does not exist



@app.route('/search', methods=['GET'])


@app.route('/admin/userpermission/change', methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)
