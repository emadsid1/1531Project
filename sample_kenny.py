from class_defines import data, user, channel, mesg, reacts
from flask import Flask, request, flash
from datetime import datetime
from json import dumps

app = Flask(__name__)

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
    sender = request.form.get('user')
    time_to_send = request.form.get('time to send')
    msg = request.form.get('message')


@app.route('/message/send', methods=['POST'])
def mesg_send():
    global data
    # counter = 0
    valid_send = False  # check if the user can actually send the message
    valid_account = False   # check if the sender is in the account list
    sending_time = datetime.now()
    sender = request.form.get('user')
    msg = request.form.get('message')
    current_channel = request.form.get('channel')
    if len(msg) > 1000:
        raise Exception('ValueError')
    else:
        for counter, acc in enumerate(data['accounts']):
            if acc == sender:
                # sender exists in the account list, get the token and channels the sender holds
                valid_account = True
                token = acc.token
                user_channels = acc.in_channel
                if token == '':
                    # if the sender is not authorised
                    raise Exception('AccessError')
                else:
                    for cha in user_channels:
                        if current_channel == cha:
                            # sender verified and add the new message to the current channel
                            valid_send = True
                    if valid_send == False:
                        # the authorised user has not joined the channel they are trying to post to
                        raise Exception('AccessError')
        if valid_account == False:
            # if the account doesn't exist in the account list
            raise Exception('AccessError')
    if valid_send == True and valid_account == True:
        for cha in user_channels:
            if cha == current_channel:
                cha.messages.append(mesg(sender, sending_time, msg, False))
                cha.messages.message_id = len(cha.messages)     # TODO not sure if this is right
                break
    return dumps({
        'message_id': cha.messages.message_id,    # TODO not sure if this is right
    })

@app.route('/message/remove', methods=['DELET'])
def mesg_remove():
    global data
    # how to find the correct original message?

@app.route('/message/edit', methods=['PUT'])
def mesg_edit():
    global data
    new_message = request.form.get('new message')
    # how to find the correct original message?
    return dumps('successfully edited the message')

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
