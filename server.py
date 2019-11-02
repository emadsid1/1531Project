"""Flask server"""
import sys
import re
import jwt
from json import dumps
from uuid import uuid4
from flask_mail import Mail, Message
from flask_cors import CORS
from flask import Flask, request
from datetime import datetime, timezone, timedelta
from Error import AccessError
from class_defines import data, user, channel, mesg, reacts
from auth_functions import *
from helper_functions import *

app = Flask(__name__)
CORS(app)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'snakeflask3@gmail.com',
    MAIL_PASSWORD = "snake.flask123"
)

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

@app.route('/auth/login', methods = ['POST'])
def route_auth_login():
    return auth_login()

@app.route('/auth/logout', methods = ['POST'])
def route_auth_logout():
    return auth_logout()

@app.route('/auth/register', methods = ['POST'])
def route_auth_register():
    return auth_register()

@app.route('/auth/passwordreset/request', methods = ['POST'])
def route_reset_request():
    return reset_request(app)

@app.route('/auth/passwordreset/reset', methods = ['POST'])
def route_reset_reset():
    return reset_reset()

@app.route('/channels/create', methods = ['POST'])
def channel_create():
    global data
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')

    #TESTING
    #data['accounts'].append(user('email', 'password', 'first', 'last', 'handle', token))
    #TESTING

    if max_20_characters(name) == False:
        raise ValueError('name is more than 20 characters')
    else:
        channel_id = int(uuid4())
        data['channels'].append(channel(name, is_public, channel_id, False))
        index = channel_index(channel_id)
        data['channels'][index].owners.append(user_from_token(token))
        data['channels'][index].members.append(user_from_token(token))

        # add channel to user's list of channels

    return dumps({
        'channel_id' : channel_id
    })

@app.route('/channel/invite', methods = ['POST'])
def channel_invite():
    #token, channel_id, u_id
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    # raise AccessError if authorised user not in channel (check_in_channel)
    # raise ValueError if channel_id doesn't exist (channel_index)
    check_in_channel(token, channel_index(channel_id)) # use Ben's funct.

    # raise ValueError if u_id doesnt refer to a valid user:TODO

    index = channel_index(channel_id)
    data['channels'][index].members.append(u_id)
    print(data['channels'][index].members)
    return dumps({
    })

@app.route('/channel/join', methods = ['POST'])
def channel_join():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if channel is Private & authorised user is not an admin
    if data['channels'][index].is_public == False:
        # check if authorised user is an admin
        valid = 0
        for admin_acc in data['channels'][index].admins:
            if admin_acc.token == token:
                valid = 1
        if valid == 0:
            raise AccessError('authorised user is not an admin of private channel')

    acct = user_from_token(token)
    data['channels'][index].members.append(acct)

    #print(data['channels'][index].members[1].token) #returns token of 2nd member (1st member is one who created channel)

    return dumps({
    })

@app.route('/channel/leave', methods = ['POST'])
def channel_leave():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    acct = user_from_token(token)
    data['channels'][index].members.pop(acct)

    if acct in data['channels'][index].owners:
        data['channels'][index].owners.pop(acct)
    if acct in data['channels'][index].admins:
        data['channels'][index].admins.pop(acct)

    return dumps({
    })

@app.route('/channel/addowner', methods = ['POST'])
def channel_add_owner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # check if user with u_id is already owner
    if user_from_uid(u_id) in data['channels'][index].owners:
        raise ValueError('User with u_id is already an owner')

    # check if authorised user is an owner of this channel
    if user_from_token(token) not in data['channels'][index].owners:
        raise AccessError('Authorised user not an owner of this channel')

    acct = user_from_uid(u_id)
    data['channels'][index].owners.append(acct)

    return dumps({
    })

@app.route('/channel/removeowner', methods = ['POST'])
def channel_remove_owner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise ValueError if u_id is not an owner
    if user_from_uid(u_id) not in data['channels'][index].owners:
        raise ValueError('u_id is not an owner of the channel')

    # raise AccessError if token is not an owner of this channel
    if user_from_token(token) not in data['channels'][index].owners:
        raise AccessError('authorised user is not an owner of this channel')

    acct = user_from_uid(u_id)
    data['channels'][index].owners.pop(acct)

    return dumps({
    })

@app.route('/channel/details', methods = ['GET'])
def channel_details():
    global data
    token = request.args.get('token')
    channel_id = request.args.get('channel_id') # supposed to be an int

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if authorised user isn't in channel
    if user_from_token(token) not in data['channels'][index].members or user_from_token(token) not in data['channels'][index].owners or user_from_token(token) not in data['channels'][index].admins:
        raise AccessError('authorised user is not in channel')

    channel_name = data['channels'][index].name
    owner_members = data['channels'][index].owners
    all_members = data['channels'][index].members

    return dumps({
        'name': channel_name,
        'owners': owner_members,
        'members': all_members
    })

@app.route('/channels/list', methods = ['GET'])
def channel_list():
    global data
    token = request.args.get('token')

    # testing set up
    #data['channels'][0].members.append(user_from_token(token))
    # testing set up

    channel_list = []
    for channel in data['channels']:
        for acct in channel.members:
            if acct.token == token:
                channel_list.append(channel.name)

    return dumps({
        'channels': channel_list
    })

@app.route('/channels/listall', methods = ['GET'])
def channel_listall():
    global data
    token = request.args.get('token')

    channel_list = []
    for channel in data['channels']:
        channel_list.append('Name: '+channel.name +' Public? '+ channel.is_public)

    return dumps({
        'channels': channel_list
    })

@app.route('/channel/messages', methods = ['GET'])
def channel_messages():
    global data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if authorised user isn't in channel
    if user_from_token(token) not in data['channels'][index].members or user_from_token(token) not in data['channels'][index].owners or user_from_token(token) not in data['channels'][index].admins:
        raise AccessError('authorised user is not in channel')

    # raise ValueError if start is greater than no. of total messages
    no_total_messages = len(data['channels'][index].messages)
    if start > no_total_messages:
        raise ValueError('start is greater than no. of total messages')

    messages = []
    i = start
    for i in data['channels'][index].messages[i]:
        message = {}
        message['message_id'] = data['channels'][index].messages[i].message_id
        message['u_id'] = data['channels'][index].messages[i].sender
        message['message'] = data['channels'][index].messages[i].message
        message['time_created'] = data['channels'][index].messages[i].create_time
        message['reacts'] = data['channels'][index].messages[i].reaction
        message['is_pinned'] = data['channels'][index].messages[i].is_pinned

        messages.append(message)
        if i == (start + 50):
            end = i
            break
        if i == no_total_messages:
            end = -1
            break

    return dumps({
        'messages': messages,
        'start': start,
        'end': end
    })

@app.route('/message/sendlater', methods=['POST'])
def send_later():
    global data
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    sent_stamp = int(request.form.get('time_sent'))
    # get the actual datetime object from a integer stamp input
    dt_sent = datetime.fromtimestamp(sent_stamp)
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    elif dt_sent < datetime.now():
        raise ValueError('Time sent is a value in the past!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # check if the sender has joined the channel
        has_joined = False
        for chan in sender.in_channel:
            if find_channel(chan) == current_channel:
                has_joined == True
        if has_joined == False:
            raise AccessError('You have not joined this channel yet, join first!')
        # generate a globally unique id
        msg_id = int(uuid4())
        while 1:
            if datetime.now() == dt_sent:
                break
        # time sent reached and no exceptions raised, send the message
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, chan_id, True))
    return dumps({
        'message_id': msg_id,
    })

@app.route('/message/send', methods=['POST'])
def mesg_send():
    global data
    sending_time = datetime.now()
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # generate a globally unique id
        msg_id = int(uuid4())
        # no exceptions raised, then add(send) the message to the current channel
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, chan_id, False))
    return dumps({
        'message_id': msg_id,
    })

@app.route('/message/remove', methods=['DELETE'])    # TODO no channel id???????
def mesg_remove():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    remover = user_from_token(token)
    found_msg = find_msg(msg_id)
    # find the channel where the message belongs to
    msg_channel = find_channel(found_msg.in_channel)
    if found_msg.sender != remover:
        raise AccessError('You do not have the permission to delete this message as you are not the sender!')
    elif (check_owner(msg_channel, remover.u_id) == False) or (check_admin(msg_channel, remover.u_id) == False):
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # no exception raised, then remove the message
    msg_channel.messages.remove(found_msg)
    return dumps({

    })

@app.route('/message/edit', methods=['PUT'])
def mesg_edit():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    new_message = request.form.get('message')
    editor = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if len(new_message) > 1000:
        raise ValueError('Message is more than 1000 words!')
    elif found_msg.sender != editor:
        raise AccessError('You do not have the permission to edit this message as you are not the sender!')
    elif (check_owner(msg_channel, editor.u_id) == False) or (check_admin(msg_channel, editor.u_id) == False):
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # edit the message if no exceptions raiseds
    found_msg.message = new_message
    return dumps({

    })

@app.route('/message/react', methods=['POST'])
def mesg_react():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    reacter = user_from_token(token)
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction != None:
        raise ValueError('This message already contains an active React!')
    # give the message a reaction if no exceptions raised
    found_msg.reaction = reacts(reacter, react_id)
    return dumps({

    })

@app.route('/message/unreact', methods=['POST'])
def mesg_unreact():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction == None:
        raise ValueError('This message does not contain an active React!')
    # unreact the message if no exceptions raised
    found_msg.reaction = None
    return dumps({

    })

@app.route('/message/pin', methods=['POST'])
def mesg_pin():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    pinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, pinner.u_id) == False:
        raise ValueError('You can not pin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == True:
        raise ValueError('The message is already pinned!')
    elif check_member(msg_channel, pinner.u_id) == False:
        raise AccessError('You can not pin the message as you are not a member of the channel')
    # pin the message if no exceptions raised
    found_msg.is_pinned = True
    return dumps({

    })

@app.route('/message/unpin', methods=['POST'])
def mesg_unpin():
    global data
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    unpinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, unpinner.u_id) == False:
        raise ValueError('You can not unpin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == False:
        raise ValueError('The message is already unpinned!')
    elif check_member(msg_channel, unpinner.u_id) == False:
        raise AccessError('You can not unpin the message as you are not a member of the channel')
    # unpin the message if no exceptions raised
    found_msg.is_pinned = False
    return dumps({

    })

@app.route('/user/profile', methods=['GET'])
def user_profile():
    global data
    token = request.args.get("token")
    valid = False
    user = {}
    for acc in data["accounts"]:
        if token == acc.token: # note: assumes token is valid
            valid = True
            if request.args.get("u_id") == acc.u_id: # supposed to be an int
                user["email"] = acc.email
                user["name_first"] = acc.name_first
                user["name_last"] = acc.name_last
                user["handle_str"] = acc.handle
            else:
                raise ValueError("Your user_id is incorrect.") # wrong u_id
    if valid == False:
        raise AccessError("Your token is invalid.") # invalid token
    return dumps({
    "email": user["email"],
    "name_first": user["name_first"],
    "name_last": user["name_last"],
    "handle_str": user["handle_str"]
    })

@app.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    global data
    token = str(request.form.get("token")) #assume token is valid

    name_first = str(request.form.get("name_first"))
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise ValueError("Your firstname is not between 1 and 50 characters in length.")

    name_last = str(request.form.get("name_last"))
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise ValueError("Your surname is not between 1 and 50 characters in length.")

    for acc in data["accounts"]:
        if token == acc.token:
            acc.name_first = name_first
            acc.name_last = name_last
        else:
            raise AccessError("Your token is invalid.") # invalid token

    return dumps({})


@app.route('/user/profile/setemail', methods=['PUT'])
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
            raise ValueError("This email is already being used by another user.") # email already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].email = email
    else:
        raise AccessError("Your token is invalid.") # token is invalid
    return dumps({})

@app.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    global data
    token = request.form.get("token") # assume token is valid
    handle = str(request.form.get("handle_str"))
    if len(handle) < 3 or len(handle) > 20:
        raise ValueError("Your handle is not between 3 and 20 characters in length.") # handle has incorrect number of chars
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if handle == acc.handle:
            raise ValueError("This handle is already being used by another user.") # handle already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].handle = handle
    else:
        raise AccessError("Your token is invalid.") #token is invalid
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
    channel = int(request.form.get("channel_id"))
    valid = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            valid = True
            if ch.is_standup == True:
                raise ValueError("A standup is already in progress.") # standup is already in progress
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise ValueError("Your channel_id does not exist.") # channel does not exist

    check_in_channel(token, ch_counter)

    data["channels"][ch_counter].is_standup = True
    data["channels"][ch_counter].standup_time = datetime.now()
    finish = data["channels"][ch_counter].standup_time + timedelta(minutes=15)
    standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()

    return dumps({
    "time_finish": standup_finish
    })

@app.route('/standup/send', methods=['POST'])
def standup_send():
    token = request.form.get("token") # assume token is valid
    channel = int(request.form.get("channel_id"))
    valid = False
    ch_counter = 0
    for ch in data["channels"]:
        if channel == ch.channel_id:
            if ch.is_standup == False:
                raise ValueError("A standup is not currently in progress.") # standup is not happening atm
            valid = True
        elif valid == False:
            ch_counter += 1
    if valid == False:
        raise ValueError("Your channel_id does not exist.") # channel does not exist

    message = request.form.get("message")
    if len(message) > 1000:
        raise ValueError("Your message is over 1000 characters in length.") # message too long

    check_in_channel(token, ch_counter)

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
    perm_id = int(request.form.get("permission_id"))
    if perm_id < 1 or perm_id > 3:
        raise ValueError("Your permission_id is not valid.") # invalid perm_id
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
        raise AccessError("Only owners and admins can change permissions.") # members cannot use this function
    if valid == False:
        raise ValueError("Your user_id is incorrect.") # user does not exist
    for add in data["channels"]:
        if perm_id == 1:
            add.owners.append(user)
        if perm_id == 2:
            add.admins.append(user)
        if perm_id == 3:
            add.members.append(user)
    return dumps({})

if __name__ == '__main__':
    app.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
