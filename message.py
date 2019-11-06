'''
Message functions by Kenny Han z5206270 (just to make pylint happy XD) <- TODO LMAO
'''
from flask import Flask, request
from json import dumps
from Error import AccessError
from datetime import datetime, timezone
from time import time
from threading import Timer
from uuid import uuid4
from class_defines import data, User, Channel, Mesg, Reacts
from helper_functions import find_channel, find_msg, check_admin, check_owner, check_member, user_from_token, user_from_uid
    
def send_later(token, msg, chan_id, sent_stamp):
    # TESTING
    # user1 = User('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = Channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(Mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING
    # make the integer stamp input float so that it can be used with the time() function
    float_time = float(sent_stamp)
    time_out = float_time - time()
    if time_out < 0:
        raise ValueError('Time sent is a value in the past!')
    # create a new thread apart from the main thread, while other function calls are still allowed
    send = Timer(time_out, msg_send, (token, msg, chan_id))
    send.start()
    return dumps('Waiting')

def msg_send(token, msg, chan_id):
    global data
    sending_time = datetime.now()
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # generate a globally unique id
        msg_id = int(uuid4())
        # no exceptions raised, then add(send) the message to the current channel
        current_channel.messages.append(Mesg(sender, sending_time, msg, msg_id, chan_id, False))
    return dumps({
        'message_id': msg_id,
    })

def msg_remove(token, msg_id):  # TODO no channel id???????
    global data
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

def msg_edit(token, msg_id, new_msg):
    global data
    editor = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    # iter3 update: if the new msg is empty, delete the message
    if new_msg == '':
        msg_remove(token, msg_id)
    elif len(new_msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    elif found_msg.sender != editor:
        raise AccessError('You do not have the permission to edit this message as you are not the sender!')
    elif (check_owner(msg_channel, editor.u_id) == False) or (check_admin(msg_channel, editor.u_id) == False):
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # edit the message if no exceptions raiseds
    found_msg.message = new_msg
    return dumps({
        
    })
    
def msg_react(token, msg_id, react_id):
    global data
    reacter = user_from_token(token)
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction != None:
        raise ValueError('This message already contains an active React!')
    # give the message a reaction if no exceptions raised
    found_msg.reaction = Reacts(reacter, react_id)
    return dumps({

    })

def msg_unreact(token, message_id, react_id):
    global data
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction == None:
        raise ValueError('This message does not contain an active React!')
    # unreact the message if no exceptions raised
    found_msg.reaction = None
    return dumps({

    })

def msg_pin(token, msg_id):
    global data
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
    
def msg_unpin(token, msg_id):
    global data
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
