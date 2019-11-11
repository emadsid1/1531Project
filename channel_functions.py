from flask import Flask, request, flash
from datetime import datetime
from json import dumps
from class_defines import data, Channel, User
from Error import AccessError
#from helper_functions import check_in_channel
from uuid import uuid4
from auth import auth_register
import jwt
import json

#TESTING:
import pytest
from Error import AccessError

app = Flask(__name__)

# given a token, returns acc with that token
#TODO: Incorporate JWT decrypt to get it working with auth
def user_from_token(token):
    global data
    for acc in data['accounts']:
        #encoded = jwt.encode({'email': acc.email}, acc.password, algorithm = 'HS256')
        #print(encoded.decode('utf-8'))
        #print("acc.token: "+acc.token)

        #if encoded.decode('utf-8') == acc.token:
        #    return acc
        #    token = jwt.encode({'email': email}, password, algorithm = 'HS256')   
        #decoded = jwt.decode(acc.token, acc.password, algorithm = 'HS256')
        #print(decoded)
        #print(decoded['email'])
        #print(type(acc.token))
        #print(type(token))
        #print("token: "+token)
        if acc.token == token:
            return acc
    raise AccessError('token does not exist for any user')

# given u_id, returns acc with that u_id
def user_from_uid(u_id):
    global data
    for acc in data['accounts']:
        if acc.u_id == u_id:
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
        #TESTING:
        #print(i.channel_id)
        if int(i.channel_id) == int(channel_id):
            return index
        index = index + 1
    
    raise ValueError('channel does not exist')

def channels_create(token, name, is_public):
    global data

    if max_20_characters(name) == False:
        raise ValueError('name is more than 20 characters')
    else: 
        channel_id = int(uuid4())
        data['channels'].append(Channel(name, is_public, channel_id, False))
        index = channel_index(channel_id)
        data['channels'][index].owners.append(user_from_token(token).u_id)
        data['channels'][index].members.append(user_from_token(token).u_id)

        # add channel to user's list of channels 
        acct = user_from_token(token)
        acct.in_channel.append(channel_id)
    
    return dumps({
        'channel_id': channel_id
    })

def test_channels_create():
    with pytest.raises(Exception): # Following should raise exceptions
        channels_create('valid token', 'This is a string that is much longer than the max length', True)

def channel_invite(token, channel_id, u_id):
    global data
    #TESTING
    #channel_id = channels_create(token, 'Channelforinv', True) #wont work since channels_create doesn't return purely an int
    #print(channel_id)

    # raise AccessError if authorised user not in channel
    # check if channel_id is part of User's in_channel list
    acct = user_from_token(token)
    #print(acct.in_channel)
    #print(channel_id)
    print(acct.in_channel)
    if (channel_id in acct.in_channel) == False:
        raise AccessError('authorised user is not in channel')

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)
    data['channels'][index].members.append(u_id)

    # add channel to user's list of channels 
    acct = user_from_uid(u_id)
    acct.in_channel.append(channel_id)

    #print(data['channels'][index].members)
    return dumps({
    })

def test_channel_invite():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail@gmail.com", "password123456", "John", "Smith"))
    token = auth_register_dict['token']

    auth_register_dict2 = json.loads(auth_register("emad@gmail.com", "password142256", "Emad", "Siddiqui"))
    token2 = auth_register_dict2['token']

    auth_register_dict3 = json.loads(auth_register("email@gmail.com", "password13456", "Firstname", "Lastname"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = json.loads(channels_create(token, "tokenchannel", True)) # create token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    channel_invite(token, channel_id, uid3)

    print(channel_id)
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token2, channel_id, uid3) #AccessError since token2 is not authorised
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, channel_id, (uid3+8)) #ValueError since u_id does not exist

def channel_join(token, channel_id):
    global data

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

def test_channel_join():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail1@gmail.com", "password123456", "John1", "Smith1"))
    token = auth_register_dict['token']

    auth_register_dict2 = json.loads(auth_register("emad1@gmail.com", "password142256", "Emad1", "Siddiqui1"))
    token2 = auth_register_dict2['token']

    auth_register_dict3 = json.loads(auth_register("email1@gmail.com", "password13456", "Firstname1", "Lastname1"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = json.loads(channels_create(token, "tokenchannel1", False)) # create PRIVATE token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_join(token2, channel_id) #channel is PRIVATE & token2 is not an admin
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist
    
def channel_leave(token, channel_id):
    global data
    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    acct = user_from_token(token)
    #print(data['channels'][index].members)
    print(acct.u_id)
    #data['channels'][index].members.pop(acct.u_id)

    for j in enumerate(data['channels'][index].members):
        if j == acct.u_id:
            #print(data['channels'][index].members[j])
            data['channels'][index].members.pop(j)


    #if acct.u_id in data['channels'][index].members:
    #    data['channels'][index].owners.pop(acct.u_id)

    #if acct.u_id in data['channels'][index].owners:
    #    data['channels'][index].owners.pop(acct.u_id)
    #if acct.u_id in data['channels'][index].admins:
    #    data['channels'][index].admins.pop(acct.u_id)

    return dumps({
    })

def test_channel_leave():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail2@gmail.com", "password123456", "John2", "Smith2"))
    token = auth_register_dict['token']

    auth_register_dict2 = json.loads(auth_register("emad2@gmail.com", "password142256", "Emad2", "Siddiqui2"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']

    auth_register_dict3 = json.loads(auth_register("email2@gmail.com", "password13456", "Firstname2", "Lastname2"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = json.loads(channels_create(token, "tokenchannel2", False)) # create PRIVATE token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_leave(token, 00000000000) #ValueError since channel_id does not exist

    #with pytest.raises(Exception): # Following should raise exceptions
    #    channel_leave(token2, channel_id) # token2 is not a part of channel_id, AccessError

    channel_invite(token, channel_id, uid2) # add token2 to channel
    channel_leave(token2, channel_id) # should work as now token2 is part of channel
    
    #TODO: ASSERT THAT data['channels'] member list only has u_id of token and not u_id of token2 

def channel_add_owner(token, channel_id, u_id):
    global data

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

def channel_remove_owner(token, channel_id, u_id):
    global data

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

def channel_details(token, channel_id):
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError('authorised user is not in channel')
    acct = user_from_token(token)
    if (channel_id in acct.in_channel) == False:
        raise AccessError('authorised user is not in channel')

    channel_name = data['channels'][index].name

    owners_uid = []
    members_uid = []

    for i in data['channels'][index].owners:
        owners_uid.append(i.u_id)
    
    for i in data['channels'][index].members:
       members_uid.append(i.u_id)
    
    return dumps({
        'name': channel_name,
        'owners': owners_uid,
        'members': members_uid
    })

def channels_list(token):
    global data

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

def channels_listall(token):
    global data

    channel_list = []
    for channel in data['channels']:
        channel_list.append(channel.name)

    return dumps({
        'channels': channel_list
    })

def channel_messages():
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if authorised user isn't in channel
    if user_from_token(token) not in data['channels'][index].members or user_from_token(token) not in data['channels'][index].owners or user_from_token(token) not in data['channels'][index].admins:
        raise AccessError('authorised user is not in channel')

    # raise ValueError if start is greater than no. of total messages
    no_total_messages = len(data['channels'][index].messages)
    if start > no_total_messages:
        raise ValueError('start is greater than no. of total messages')
    
    messages = []
    i = start
    for i in data['channels'][index].messages[i]:
        message = {}
        message['message_id'] = data['channels'][index].messages[i].message_id
        message['u_id'] = data['channels'][index].messages[i].sender
        message['message'] = data['channels'][index].messages[i].message
        message['time_created'] = data['channels'][index].messages[i].create_time
        message['reacts'] = data['channels'][index].messages[i].reaction
        message['is_pinned'] = data['channels'][index].messages[i].is_pinned

        messages.append(message)
        if i == (start + 50):
            end = i
            break
        if i == no_total_messages:
            end = -1
            break
    
    return dumps({
        'messages': messages,
        'start': start,
        'end': end
    })

if __name__ == '__main__':
    app.run(port = 5022, debug=True)
