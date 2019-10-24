"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request

app = Flask(__name__)
CORS(app)

@app.route('/auth/register', methods=['POST'])
def echo4():
    pass

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

@app.route('/auth/login', methods=['POST'])


@app.route('/auth/logout', methods=['POST'])


@app.route('/auth/register', methods=['POST'])


@app.route('/auth/passwordreset/request', methods=['POST'])


@app.route('/auth/passwordreset/reset', methods=['POST'])


@app.route('/channel/invite', methods=['POST'])


@app.route('/channel/details', methods=['GET'])


@app.route('/channel/messages', methods=['GET'])


@app.route('/channel/leave', methods=['POST'])


@app.route('/channel/join', methods=['POST'])


@app.route('/channel/addowner', methods=['POST'])


@app.route('/channel/removeowner', methods=['POST'])


@app.route('/channels/list', methods=['GET'])


@app.route('/channels/listall', methods=['GET'])


@app.route('/channels/create', methods=['POST'])


@app.route('/message/sendlater', methods=['POST'])


@app.route('/message/send', methods=['POST'])


@app.route('/message/remove', methods=['DELET'])


@app.route('/message/edit', methods=['PUT'])


@app.route('/message/react', methods=['POST'])


@app.route('/message/unreact', methods=['POST'])


@app.route('/message/pin', methods=['POST'])


@app.route('/message/unpin', methods=['POST'])


@app.route('/user/profile', methods=['GET'])


@app.route('/user/profile/setname', methods=['PUT'])


@app.route('/user/profile/setemail', methods=['PUT'])


@app.route('/user/profile/sethandle', methods=['PUT'])


@app.route('/user/profiles/uploadphoto', methods=['POST'])


@app.route('/standup/start', methods=['POST'])


@app.route('/standup/send', methods=['POST'])


@app.route('/search', methods=['GET'])


@app.route('/admin/userpermission/change', methods=['POST'])


if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)
=======
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
>>>>>>> COMP1531/19T3-cs1531-project-master
