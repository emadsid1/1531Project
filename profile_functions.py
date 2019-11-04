from json import dumps
from flask import Flask, request
from class_defines import user, channel, mesg, reacts #data
from datetime import datetime, timedelta, timezone
from Error import AccessError
import re

nom = User("naomizhen@gmail.com", "password", "naomi", "zhen", "nomHandle", "12345", 1)
ben = User("benkah@gmail.com", "password", "ben", "kah", "benHandle", "1234", 2)
chan1 = channel("chatime", True, 1, 5)

data = {
    "accounts": [nom, ben],
    "channels": [chan1]
}

def user_profile():
    global data
    token = request.args.get("token")
    valid = False
    user = {}
    for acc in data["accounts"]:
        if token == acc.token: # note: assumes token is valid
            valid = True
            if int(request.args.get("u_id")) == acc.u_id:
                user["email"] = acc.email
                user["name_first"] = acc.name_first
                user["name_last"] = acc.name_last
                user["handle_str"] = acc.handle
            else:
                raise Exception("ValueError") # wrong u_id
    if valid == False:
        raise Exception("AccessError") # invalid token
    return dumps({
    "email": user["email"],
    "name_first": user["name_first"],
    "name_last": user["name_last"],
    "handle_str": user["handle_str"]
    })

def user_profile_setname():
    global data
    token = str(request.form.get("token")) #assume token is valid

    name_first = str(request.form.get("name_first"))
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise Exception("ValueError")

    name_last = str(request.form.get("name_last"))
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise Exception("ValueError")

    for acc in data["accounts"]:
        if token == acc.token:
            acc.name_first = name_first
            acc.name_last = name_last
        else:
            raise Exception("AccessError") # invalid token

    return dumps({})


def user_profile_email():
    global data
    token = request.form.get("token") # assume token is valid
    email = request.form.get("email")
    check_email(email)
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if email == acc.email:
            raise Exception("ValueError") # email already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].email = email
    else:
        raise Exception("AccessError") # token is invalid
    return dumps({})

def user_profile_sethandle():
    global data
    token = request.form.get("token") # assume token is valid
    handle = str(request.form.get("handle_str"))
    if len(handle) < 3 or len(handle) > 20:
        raise Exception("ValueError") # handle has incorrect number of chars
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if handle == acc.handle:
            raise Exception("ValueError") # handle already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].handle = handle
    else:
        raise Exception("AccessError") #token is invalid
    return dumps({})

# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def user_profile_uploadphoto():
    request = request.get("img_url")
    if request != 200:
        raise Exception("ValueError")
    url = request.form.get("img_url")
    # how to get image size?
    return dumps({})

def users_all():
    pass

def standup_start():
    token = request.form.get("token") #assume token is valid
    channel = int(request.form.get("channel_id"))
    valid = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            valid = True
            if ch.is_standup == True:
                raise Exception("AccessError") # standup is already in progress
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise Exception("ValueError") # channel does not exist

    check_in_channel(token, ch_counter)

    data["channels"][ch_counter].is_standup = True
    data["channels"][ch_counter].standup_time = datetime.now()
    finish = data["channels"][ch_counter].standup_time + timedelta(minutes=15)
    standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()

    return dumps({
    "time_finish": standup_finish
    })

def standup_send():
    token = request.form.get("token") # assume token is valid
    channel = int(request.form.get("channel_id"))
    valid = False
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

    check_in_channel(token, ch_counter)

    # TODO: how to check if standup has finished?
    data["channels"][ch_counter].standup_messages.append(message)
    return dumps({})

def standup_active():
    pass

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

def admin_userpermission_change():
    perm_id = int(request.form.get("permission_id"))
    if perm_id < 1 or perm_id > 3:
        raise Exception("ValueError") # invalid perm_id
    user_id = int(request.form.get("u_id"))
    valid = False
    has_permission = False
    token = request.form.get("token") # assume token is valid
    for ch in data["channels"]:
        for own in ch.owners:
            if token == own.token:
                has_permission = True
            if user_id == acc.user_id:
                valid = True
                if perm_id != 1:
                    remove(own)
                    user = own
        for ad in ch.admins:
            if token == ad.token:
                has_permission = True
            if user_id == acc.user_id:
                valid = True
                if perm_id != 2:
                    remove(acc)
                    user = acc
        for mem in ch.members:
            if user_id == acc.user_id:
                valid = True
                if perm_id != 3:
                    remove(mem)
                    user = mem
    if has_permission == False:
        raise Exception("AccessError") # members cannot use this function
    if valid == False:
        raise Exception("ValueError") # user does not exist
    for add in data["channels"]:
        if perm_id == 1:
            add.owners.append(user)
        if perm_id == 2:
            add.admins.append(user)
        if perm_id == 3:
            add.members.append(user)
    return dumps({})

# Helper functions
def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not(re.search(regex,email))):    # if not valid email
        raise Exception('ValueError')

def check_in_channel(token, channel_index):
    in_channel = False
    for acc in data["channels"][channel_index].owners: # search owners list
        if token == acc.token:
            in_channel = True
    if in_channel == False:
        for acc in data["channels"][channel_index].admins: # search admins list
            if token == acc.token:
                in_channel = True
    if in_channel == False:
        for acc in data["channels"][channel_index].members: # search members list
            if token == acc.token:
                in_channel = True
    if in_channel == False: # if the user is not in the channel, raise an error
        raise Exception("AccessError") # TODO: need to write this function

if __name__ == '__main__':
    app.run(debug=True)
