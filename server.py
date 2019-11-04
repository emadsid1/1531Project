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
def route_user_profile():
    global data
    token = request.args.get("token")
    user_id = user_from_token(token)
    return user_profile(token, user_id)

@app.route('/user/profile/setname', methods=['PUT'])
def route_user_profile_setname():
    global data
    token = request.form.get("token")
    name_first = request.form.get("name_first")
    name_last = request.form.get("name_last")
    return user_profile_setname(token, name_first, name_last)

@app.route('/user/profile/setemail', methods=['PUT'])
def route_user_profile_email():
    token = request.form.get("token")
    email = request.form.get("email")
    return user_profile_email(token, email)

@app.route('/user/profile/sethandle', methods=['PUT'])
def route_user_profile_sethandle():
    token = request.form.get("token")
    handle = request.form.get("handle_str")
    return user_profile_sethandle(token, handle)

@app.route('/user/profiles/uploadphoto', methods=['POST'])
# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def route_user_profile_uploadphoto():
    return user_profile_uploadphoto()

@app.route('/users/all', methods=['GET'])
def route_users_all():
    return users_all()

@app.route('/standup/start', methods=['POST'])
def route_standup_start():
    token = request.form.get("token")
    channel = request.form.get("channel_id")
    length = request.form.get("length")
    return standup_start(token, channel, length)

@app.route('/standup/active', methods=['GET'])
def route_standup_active():
    return standup_active()

@app.route('/standup/send', methods=['POST'])
def route_standup_send():
    token = request.form.get("token")
    channel = request.form.get("channel_id")
    message = request.form.get("message")
    return standup_send(token, channel, message)

@app.route('/search', methods=['GET'])
def route_search():
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    return search(token, query_str)

@app.route('/admin/userpermission/change', methods=['POST'])
def route_admin_userpermission_change():
    token = request.args.get("token")
    user_id = int(request.form.get("u_id"))
    perm_id = int(request.form.get("permission_id"))
    return admin_userpermission_change(token, user_id, perm_id)

if __name__ == '__main__':
    app.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
