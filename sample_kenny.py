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
def find_channel(channel_id):
    global data
    channel_found = False
    for cha in data['channels']:
        if cha.channel_id == channel_id:
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
    valid_send = False  # check if the user can actually send the message
    valid_account = False   # check if the sender is in the account list
    sender = request.form.get('user')
    time_to_send = request.form.get('time to send')
    msg = request.form.get('message')

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
        current_channel = find_channel
        msg_id = str(uuid4())
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, False))
    return dumps({
        'message_id': msg_id,    # TODO not sure if this is right
    })

@app.route('/message/remove', methods=['DELET'])
def mesg_remove():
    global data
    remover = request.form.get('user')
    current_channel = request.form.get('channel')

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
