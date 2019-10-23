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


@app.route('/message/send', methods=['POST'])
def send():
    global Messages
    # check TOKEN???
    mesg = request.form.get('message')
    # get user???
    sending_time = datetime.now()
    Messages.append(Mesg(sender, sending_time, mesg))
    return dumps('message sent')


@app.route('/message/remove', methods=['DELET'])


@app.route('/message/edit', methods=['PUT'])


@app.route('/message/react', methods=['POST'])


@app.route('/message/unreact', methods=['POST'])


@app.route('/message/pin', methods=['POST'])


@app.route('/message/unpin', methods=['POST'])



if __name__ == '__main__':
    app.run(debug=True)
