from flask import Flask, request, flash
from datetime import datetime
from json import dumps
from class_defines import data, channel, user
from Error import AccessError
from sample_ben import check_in_channel

app = Flask(__name__)
#channel invite vs join, invite needed to join a private channel. passive v active.

# given a token, returns acc with that token
def user_from_token(token):
    global data
    for acc in data['accounts']:
        #print(acc)
        if acc.token == token:
            return acc
    raise AccessError('token does not exist for any user')

# given u_id, returns acc with that u_id
def user_from_uid(u_id):
    global data
    for acc in enumerate(data['accounts']):
        if int(acc.user_id) == int(u_id):
            return acc
    raise AccessError('u_id does not exist for any user')

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

    #TESTING
    #data['accounts'].append(user('email', 'password', 'first', 'last', 'handle', token))
    #TESTING

    if max_20_characters(name) == False:
        raise ValueError('name is more than 20 characters')
    else: 
        channel_id = hash(name)  #assume channel_id is hash of name
        data['channels'].append(channel(name, is_public, channel_id, False))
        index = channel_index(channel_id)
        data['channels'][index].owners.append(user_from_token(token))
        data['channels'][index].members.append(user_from_token(token))

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
    u_id = int(request.form.get('u_id'))

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
    if data['channels'][index].is_public == False:
        # check if authorised user is an admin
        valid = 0
        for admin_acc in data['channels'][index].admins: 
            if admin_acc.token == token:
                valid = 1
        if valid == 0:
            raise AccessError('authorised user is not an admin of private channel')

    acct = user_from_token(token)
    data['channels'][index].members.append(acct)

    #print(data['channels'][index].members[1].token) #returns token of 2nd member (1st member is one who created channel)

    return dumps({
    })

@app.route('/channel/leave', methods = ['POST'])
def channel_leave():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    acct = user_from_token(token)
    data['channels'][index].members.pop(acct)

    if acct in data['channels'][index].owners:
        data['channels'][index].owners.pop(acct)
    if acct in data['channels'][index].admins:
        data['channels'][index].admins.pop(acct)

    return dumps({
    })

@app.route('/channel/addowner', methods = ['POST'])
def channel_add_owner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # check if user with u_id is already owner 
    if user_from_uid(u_id) in data['channels'][index].owners:
        raise ValueError('User with u_id is already an owner')

    # check if authorised user is an owner of this channel
    if user_from_token(token) not in data['channels'][index].owners:
        raise AccessError('Authorised user not an owner of this channel')
    
    acct = user_from_uid(u_id)
    data['channels'][index].owners.append(acct)

    return dumps({
    })

@app.route('/channel/removeowner', methods = ['POST'])
def channel_remove_owner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise ValueError if u_id is not an owner
    if user_from_uid(u_id) not in data['channels'][index].owners:
        raise ValueError('u_id is not an owner of the channel')

    # raise AccessError if token is not an owner of this channel
    if user_from_token(token) not in data['channels'][index].owners:
        raise AccessError('authorised user is not an owner of this channel')
    
    acct = user_from_uid(u_id)
    data['channels'][index].owners.pop(acct)

    return dumps({
    })

@app.route('/channel/details', methods = ['GET'])
def channel_details():
    global data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if authorised user isn't in channel
    if user_from_token(token) not in data['channels'][index].members or user_from_token(token) not in data['channels'][index].owners or user_from_token(token) not in data['channels'][index].admins:
        raise AccessError('authorised user is not in channel')

    name = data['channels'][index].name
    owner_members = data['channels'][index].owners
    all_members = data['channels'][index].members

    return dumps({
        'name': channel_name,
        'owners': owner_members,
        'members': all_members
    })

@app.route('/channel/list', methods = ['GET'])
def channel_list():
    global data
    token = request.args.get('token')

    # testing set up
    #data['channels'][0].members.append(user_from_token(token))
    # testing set up

    channel_list = []
    for channel in data['channels']:
        for acct in channel.members:
            if acct.token == token:
                channel_list.append(channel.name)

    return dumps({
        'channels': channel_list
    })

@app.route('/channel/listall', methods = ['GET'])
def channel_listall():
    global data
    token = request.args.get('token')

    channel_list = []
    for channel in data['channels']:
        channel_list.append('Name: '+channel.name +' Public? '+ channel.is_public)

    return dumps({
        'channels': channel_list
    })

@app.route('/channel/messages', methods = ['GET'])
def channel_messages():
    global data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    no_messages = 0
    
    
    return dumps({
    })

if __name__ == '__main__':
    app.run(port = 5022, debug=True)