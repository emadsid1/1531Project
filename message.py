'''
Message functions by Kenny Han z5206270 (just to make pylint happy XD) <- TODO LMAO
'''
from json import dumps
from exception import ValueError, AccessError
from datetime import datetime, timezone
from time import time
from threading import Timer
from class_defines import data, User, Channel, Mesg, Reacts
from helper_functions import find_channel, find_msg, check_admin, check_owner, check_member, user_from_token, user_from_uid
    
def send_later(token, msg, chan_id, sent_stamp):
    # get the number of second of the waiting interval for sending the msg later
    later_period = sent_stamp - datetime.now().replace(tzinfo=timezone.utc).timestamp()
    if later_period < 0:
        raise ValueError(description='Time sent is a value in the past!')
    # create a new thread apart from the main thread, while other function calls are still allowed
    send = Timer(later_period, msg_send, (token, msg, chan_id))
    send.start()

def msg_send(token, msg, chan_id):
    global data
    sending_time = datetime.now()
    print(sending_time)
    sender = user_from_token(token)
    current_channel = find_channel(chan_id)
    if len(msg) > 1000:
        raise ValueError(description='Message is more than 1000 words!')
    elif check_member(current_channel, sender.u_id) == False:
        raise AccessError(description='You have not joined this channel yet, please join first!')
    else:
        # generate an unique id
        data['message_count'] += 1
        msg_id = data['message_count']
        # no exceptions raised, then add(send) the message to the current channel
        current_channel.messages.append(Mesg(sender.u_id, sending_time, msg, msg_id, chan_id, False))
    return {'message_id': msg_id}

def msg_remove(token, msg_id):
    global data
    remover = user_from_token(token)
    found_msg = find_msg(msg_id)
    # find the channel where the message belongs to
    msg_channel = find_channel(found_msg.in_channel)
    if found_msg.sender != remover:
        raise AccessError(description='You do not have the permission to delete this message as you are not the sender!')
    elif (check_owner(msg_channel, remover.u_id) == False) or (check_admin(msg_channel, remover.u_id) == False):
        raise AccessError(description='You do not have the permission as you are not the owner or admin of this channel!')
    # no exception raised, then remove the message
    msg_channel.messages.remove(found_msg)
    return {}

def msg_edit(token, msg_id, new_msg):
    global data
    editor = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    # iter3 update: if the new msg is empty, delete the message
    if new_msg == '':
        msg_remove(token, msg_id)
    elif len(new_msg) > 1000:
        raise ValueError(description='Message is more than 1000 words!')
    elif found_msg.sender != editor:
        raise AccessError(description='You do not have the permission to edit this message as you are not the sender!')
    elif (check_owner(msg_channel, editor.u_id) == False) or (check_admin(msg_channel, editor.u_id) == False):
        raise AccessError(description='You do not have the permission as you are not the owner or admin of this channel!')
    # edit the message if no exceptions raiseds
    found_msg.message = new_msg
    return {}
    
def msg_react(token, msg_id, react_id):
    global data
    reacter = user_from_token(token)
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError(description='Invalid React ID!')
    elif found_msg.reaction != None:
        raise ValueError(description='This message already contains an active React!')
    # give the message a reaction if no exceptions raised
    found_msg.reaction = Reacts(reacter, react_id)
    return {}

def msg_unreact(token, message_id, react_id):
    global data
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError(description='Invalid React ID!')
    elif found_msg.reaction == None:
        raise ValueError(description='This message does not contain an active React!')
    # unreact the message if no exceptions raised
    found_msg.reaction = None
    return {}

def msg_pin(token, msg_id):
    global data
    pinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, pinner.u_id) == False:
        raise ValueError(description='You can not pin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == True:
        raise ValueError(description='The message is already pinned!')
    elif check_member(msg_channel, pinner.u_id) == False:
        raise AccessError(description='You can not pin the message as you are not a member of the channel')
    # pin the message if no exceptions raised
    found_msg.is_pinned = True
    return {}
    
def msg_unpin(token, msg_id):
    global data
    unpinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, unpinner.u_id) == False:
        raise ValueError(description='You can not unpin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == False:
        raise ValueError(description='The message is already unpinned!')
    elif check_member(msg_channel, unpinner.u_id) == False:
        raise AccessError(description='You can not unpin the message as you are not a member of the channel')
    # unpin the message if no exceptions raised
    found_msg.is_pinned = False
    return {}
