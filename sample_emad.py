from flask import Flask, request, flash
from datetime import datetime
from json import dumps
from class_defines import data, channel
from Error import AccessError

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
        data['channels'].append(channel(name, is_public, channel_id))
        index = channel_index(channel_id)
        data['channels'][index].owners = [token]
        data['channels'][index].members = [token]

        # add channel to user's list of channels 

    return dumps({
        'channel_id' : channel_id
    })

def is_member_in_channel(token, channel_id):
    global data
    for i in data['channels']:
        if i.channel_id == channel_id:
            if token in i.members:
                return True
    return False 

@app.route('/channel/invite', methods = ['POST'])
def channel_invite():
    #token, channel_id, u_id
    global data
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    #if is_member_in_channel(token, channel_id) == False: 
    #    raise AccessError('Authorised user is not already part of channel')

    #ValueError if u_id doesnt refer to a valid user ** 

    # token refers to the person giving out the invitation
    # token must be part of channel_id
    # u_id is the person receiving the invitation
    # ud_id must be a valid user
    index = channel_index(channel_id) #will raise ValueError if channel_id doesn't exist
    data['channels'][index].members.append(u_id)
    print(data['channels'][index].members)
    return dumps({
    })

@app.route('/channel/owner', methods = ['POST'])
def channel_add_owner():
    global data
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    index = channel_index(channel_id)
    data['channels'][index].owners.append(u_id)

    return dumps({
    })



if __name__ == '__main__':
    app.run(port = 5022, debug=True)