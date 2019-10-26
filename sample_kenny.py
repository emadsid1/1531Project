from flask import Flask, request, flash
from datetime import datetime
from uuid import uuid4
from json import dumps
from Error import AccessError
from class_defines import data, user, channel, mesg, reacts
from sample_emad import user_from_token, user_from_uid

app = Flask(__name__)

# helper functions

# find the correct channel base on the channel_id
def find_channel(chan_id):
    global data
    channel_found = False
    for cha in data['channels']:
        if cha.channel_id == chan_id:
            channel_found = True
            return cha
    if channel_found == False:
        raise AccessError('Channel does not exit, please join or create a channel first!')

# find the correct message base on the message_id
def find_msg(channel, msg_id):
    global data
    message_found = False
    for msg in channel.messages:
        if msg.message_id == msg_id:
            message_found = True
            return msg
    if message_found == False:
        raise AccessError('Message does not exist in current channel!')

# check if a user is an admin or an owner of a given channel
def check_owner_admin(channel, user_id):
    global data
    for u_id in channel.admins:
        if u_id = user_id:
            return True
    for u_id in channel.owners:
        if u_id = user_id:
            return True
    return False

# end of helper functions

@app.route('/echo/post', methods = ['POST'])
def echo_post():
    echo_input = request.form.get('echo')
    return dumps({'echo': echo_input})

@app.route('/echo/get', methods = ['GET'])
def echo_get():
    echo_input = requets.args.get('echo')
    return dumps({'echo': echo_input})

@app.route('/message/sendlater', methods=['POST'])
def send_later():
    global data
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = request.form.get('channel id')
    time_sent = request.form.get('time sent')
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        msg_id = str(uuid4())
        while 1:                                    # TODO not sure if this is right
            if datetime.now() = time_sent:
                break
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
    chan_id = request.form.get('channel id')
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # generate a globally unique id
        msg_id = str(uuid4())
        # no exceptions raised, then add(send) the message to the current channel
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, chan_id, False))
    return dumps({
        'message_id': msg_id,
    })

@app.route('/message/remove', methods=['DELET'])    # TODO no channel id???????
def mesg_remove():
    global data
    token = request.form.get('token')
    msg_id = request.form.get('message id')
    remover = user_from_token(token)
    found_msg = find_msg(msg_id)
    # find the channel where the message belongs to
    msg_channel = find_channel(found_msg.in_channel)
    if found_msg.sender != remover:
        raise AccessError('You do not have the permission to delete this message as you are not the sender!')
    elif check_owner_admin(msg_channel, remover.user_id) == False:
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # no exception raised, then remove the message
    msg_channel.messages.remove(found_msg)
    return dumps

@app.route('/message/edit', methods=['PUT'])
def mesg_edit():
    global data
    new_message = request.form.get('new message')
    # how to find the correct original message?
    

@app.route('/message/react', methods=['POST'])
def mesg_react():
    global data
    new_reaction = request.form.get('reaction')
    # how to find the correct original message?


@app.route('/message/unreact', methods=['POST'])
def mesg_unreact():
    global data
    # how to find the correct original message?



@app.route('/message/pin', methods=['POST'])
def mesg_pin():
    global messages
    # how to find the correct original message?


@app.route('/message/unpin', methods=['POST'])
def mesg_unpin():
    global messages
    # how to find the correct original message?


if __name__ == '__main__':
    app.run(debug=True)
