"""Flask server"""
import sys
from json import dumps
from uuid import uuid4
from flask_mail import Mail, Message
from flask_cors import CORS
from flask import Flask, request
from Error import AccessError
from class_defines import data, User, Channel, Mesg, Reacts
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from message import send_later, msg_send, msg_remove, msg_edit, msg_pin, msg_unpin, msg_react, msg_unreact
from profile import user_profile, user_profile_setname, user_profile_email, user_profile_sethandle, user_profile_uploadphoto, users_all, standup_start, standup_active, standup_send, search, admin_userpermission_change, standup_end
from channel_functions import channels_create, channel_invite, channel_join, channel_leave, channel_add_owner, channel_remove_owner, channel_details, channels_list, channels_listall, channel_messages
from helper_functions import * # TODO CHANGE LATER, KEEP FOR NOW

app = Flask(__name__)
CORS(app)
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
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
    email = request.form.get('email')
    password = request.form.get('password')
    return auth_login(email, password)

@app.route('/auth/logout', methods = ['POST'])
def route_auth_logout():
    token = request.form.get('token')
    return auth_logout(token)

@app.route('/auth/register', methods = ['POST'])
def route_auth_register():
    email = request.form.get('email')
    password = request.form.get('password')
    first = request.form.get('name_first')
    last = request.form.get('name_last')
    return auth_register(email, password, first, last)

@app.route('/auth/passwordreset/request', methods = ['POST'])
def route_reset_request():
    email = request.form.get('email')
    return reset_request(app, email)

@app.route('/auth/passwordreset/reset', methods = ['POST'])
def route_reset_reset():
    code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    return reset_reset(code, new_password)

@app.route('/channels/create', methods = ['POST'])
def route_channels_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return channels_create(token, name, is_public)

@app.route('/channel/invite', methods = ['POST'])
def route_channel_invite():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return channel_invite(token, channel_id, u_id)

@app.route('/channel/join', methods = ['POST'])
def route_channel_join():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return channel_join(token, channel_id)

@app.route('/channel/leave', methods = ['POST'])
def route_channel_leave():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return channel_leave(token, channel_id)

@app.route('/channel/addowner', methods = ['POST'])
def route_channel_add_owner():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return channel_add_owner(token, channel_id, u_id)

@app.route('/channel/removeowner', methods = ['POST'])
def route_channel_remove_owner():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return channel_remove_owner(token, channel_id, u_id)

@app.route('/channel/details', methods = ['GET'])
def route_channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id') # supposed to be an int
    return channel_details(token, channel_id)

@app.route('/channels/list', methods = ['GET'])
def route_channels_list():
    token = request.args.get('token')
    return channels_list(token)

@app.route('/channels/listall', methods = ['GET'])
def route_channels_listall():
    token = request.args.get('token')
    return channels_listall(token)

@app.route('/channel/messages', methods = ['GET'])
def route_channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return channel_messages(token, channel_id, start)

@app.route('/message/sendlater', methods=['POST'])
def route_send_later():
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    sent_stamp = int(request.form.get('time_sent'))
    return send_later(token, msg, chan_id, sent_stamp)

@app.route('/message/send', methods=['POST'])
def route_msg_send():
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    return msg_send(token, msg, chan_id)

@app.route('/message/remove', methods=['DELETE'])
def route_msg_remove():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    return msg_remove(token, msg_id)

@app.route('/message/edit', methods=['PUT'])
def route_msg_edit():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    new_message = request.form.get('message')
    return msg_edit(token, msg_id, new_message)

@app.route('/message/react', methods=['POST'])
def route_msg_react():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return msg_react(token, msg_id, react_id)

@app.route('/message/unreact', methods=['POST'])
def route_msg_unreact():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return msg_unreact(toekn, msg_id, react_id)

@app.route('/message/pin', methods=['POST'])
def route_msg_pin():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    return msg_pin(token, msg_id)

@app.route('/message/unpin', methods=['POST'])
def route_msg_unpin():
    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    return msg_unpin(token, msg_id)

@app.route('/user/profile', methods=['GET'])
def route_user_profile():
    global data
    token = request.args.get("token")
    user_id = request.args.get("u_id")
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
    token = request.args.get("token")
    return users_all(token)

@app.route('/standup/start', methods=['POST'])
def route_standup_start():
    token = request.form.get("token")
    channel = request.form.get("channel_id")
    length = request.form.get("length")
    return standup_start(token, channel, length)

@app.route('/standup/active', methods=['GET'])
def route_standup_active():
    token = request.form.get("token")
    channel = request.form.get("channel_id")
    return standup_active(token, channel)

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
