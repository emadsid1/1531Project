from flask import Flask, request, flash
from datetime import datetime
from json import dumps
from class_defines import data, channel
from Error import AccessError
from sample_ben import check_in_channel

app = Flask(__name__)
#channel invite vs join, invite needed to join a private channel. passive v active.

def max_20_characters(name):
    if len(name) <= 20:
        return True 
    else:
        return False

def channel_index(channel_id):
    global data
    index = 0
    for i in data['channels']:
        if i.channel_id == channel_id:
            return index
        index = index + 1
    raise ValueError('channel does not exist')

@app.route('/channel/create', methods = ['POST'])
def channel_create():
    global data
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public') 

    if max_20_characters(name) == False:
        raise ValueError('name is more than 20 characters')
    else: 
        channel_id = hash(name)  #assume channel_id is hash of name
        data['channels'].append(channel(name, is_public, channel_id, False))
        index = channel_index(channel_id)
        data['channels'][index].owners = [token]
        data['channels'][index].members = [token]
        print(type(channel_id))
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
    u_id = request.form.get('u_id')

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
    if data['channels'][index].is_public == True:
        # check if authorised user is an admin

    #TODO: find way to get u_id from token, write a function that when given a token, it returns u_id
    u_id = token
    data['channels'][index].members.append(u_id)

    return dumps({
    })

@app.route('/channel/leave', methods = ['POST'])
def channel_leave():
    global data
    return dumps({
    })

@app.route('/channel/addowner', methods = ['POST'])
def channel_add_owner():
    global data
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    index = channel_index(channel_id)
    data['channels'][index].owners.append(u_id)

    return dumps({
    })

@app.route('/channel/removeowner', methods = ['POST'])
def channel_remove_owner():
    global data
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')


    return dumps({
    })

@app.route('/channel/details', methods = ['GET'])
def channel_details():
    global data
    return dumps({
    })

@app.route('/channel/messages', methods = ['GET'])
def channel_messages():
    global data
    return dumps({
    })

@app.route('/channel/list', methods = ['GET'])
def channel_list():
    global data
    return dumps({
    })

@app.route('/channel/listall', methods = ['GET'])
def channel_listall():
    global data
    return dumps({
    })


if __name__ == '__main__':
    app.run(port = 5022, debug=True)