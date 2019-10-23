from flask import Flask, request, flash
from datetime import datetime
from json import dumps

app = Flask(__name__)

# global varaiables
# created a class called Mesg which stores all the information of every message
class Mesg:
    def __init__(self, sender, create_time, message):
        self.message = message
        self.sender = sender
        self.create_time = create_time
        self.reaction = None
        self.pin = False

    def get_mesg():
        return self.message

    def get_sender():
        return self.sender

    def get_mesg_time():
        return self.create_time

    def set_reaction(self, reaction):
        self.reaction = reaction

    def remove_reaction(self):
        self.reaction = None

    def pin_self(self):
        self.pin = True

    def unpin_self(self):
        self.pin = False

# a list of messages
Messages = []
# end of global variable

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
    global Messages
    # check TOKEN???
    # get user???
    latency = request.form.get('send later')
    mesg = request.form.get('message')


@app.route('/message/send', methods=['POST'])
def mesg_send():
    global Messages
    # check TOKEN???
    # get user???
    mesg = request.form.get('message')
    sending_time = datetime.now()
    if len(mesg) < 1000 or len(mesg) == 1000:
        Messages.append(Mesg(sender, sending_time, mesg))
        return dumps('message sent')
    else:
        return dumps('message not send due to some error')

@app.route('/message/remove', methods=['DELET'])
def mesg_remove():
    global Messages
    # how to find the correct original message?

@app.route('/message/edit', methods=['PUT'])
def mesg_edit():
    global Messages
    new_message = request.form.get('new message')
    # how to find the correct original message?
    return dumps('successfully edited the message')

@app.route('/message/react', methods=['POST'])
def mesg_react():
    global Messages
    new_reaction = request.form.get('reaction')
    # how to find the correct original message?


@app.route('/message/unreact', methods=['POST'])
def mesg_unreact():
    global Messages
    # how to find the correct original message?



@app.route('/message/pin', methods=['POST'])
def mesg_pin():
    global Messages
    # how to find the correct original message?


@app.route('/message/unpin', methods=['POST'])
def mesg_unpin():
    global Messages
    # how to find the correct original message?


if __name__ == '__main__':
    app.run(debug=True)
