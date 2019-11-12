from flask import Flask, request, flash
from class_defines import data, Channel, User, Mesg
from exception import ValueError, AccessError
from auth import auth_register
import json
from message import msg_send
from helper_functions import user_from_uid, max_20_characters, user_from_token, channel_index

#TESTING:
import pytest
#from Error import AccessError

app = Flask(__name__)

def channels_create(token, name, is_public):
    global data

    if max_20_characters(name) == False:
        raise ValueError(description = 'name is more than 20 characters')
    channel_id = data['channel_count']
    data['channel_count'] += 1
    data['channels'].append(Channel(name, is_public, channel_id))
    index = channel_index(channel_id)
    data['channels'][index].owners.append(user_from_token(token).u_id)
    data['channels'][index].members.append(user_from_token(token).u_id)

    # add channel to user's list of channels 
    acct = user_from_token(token)
    acct.in_channel.append(channel_id)
    
    return {
        'channel_id': channel_id
    }

# def test_channels_create():
#     with pytest.raises(Exception): # Following should raise exceptions
#         channels_create('valid token', 'This is a string that is much longer than the max length', True)

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
        raise AccessError(description = 'authorised user is not in channel')

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)
    data['channels'][index].members.append(u_id)

    # add channel to user's list of channels 
    acct = user_from_uid(u_id)
    acct.in_channel.append(channel_id)

    #print(data['channels'][index].members)
    return {
    }

# def test_channel_invite():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail@gmail.com", "password123456", "John", "Smith"))
#     token = auth_register_dict['token']

#     auth_register_dict2 = json.loads(auth_register("emad@gmail.com", "password142256", "Emad", "Siddiqui"))
#     token2 = auth_register_dict2['token']

#     auth_register_dict3 = json.loads(auth_register("email@gmail.com", "password13456", "Firstname", "Lastname"))
#     uid3 = auth_register_dict3['u_id']

#     channel_dict = channels_create(token, "tokenchannel", True) # create token's channel
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     channel_invite(token, channel_id, uid3)
    
#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_invite(token2, channel_id, uid3) #AccessError since token2 is not authorised
    
#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist
    
#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_invite(token, channel_id, (uid3+8)) #ValueError since u_id does not exist

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
            raise AccessError(description = 'authorised user is not an admin of private channel')

    acct = user_from_token(token)
    data['channels'][index].members.append(acct)

    #print(data['channels'][index].members[1].token) #returns token of 2nd member (1st member is one who created channel)

    return {
    }

# def test_channel_join():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail1@gmail.com", "password123456", "John1", "Smith1"))
#     token = auth_register_dict['token']

#     auth_register_dict2 = json.loads(auth_register("emad1@gmail.com", "password142256", "Emad1", "Siddiqui1"))
#     token2 = auth_register_dict2['token']

#     auth_register_dict3 = json.loads(auth_register("email1@gmail.com", "password13456", "Firstname1", "Lastname1"))
#     uid3 = auth_register_dict3['u_id']

#     channel_dict = channels_create(token, "tokenchannel1", False) # create PRIVATE token's channel
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_join(token2, channel_id) #channel is PRIVATE & token2 is not an admin
    
#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist
    
def channel_leave(token, channel_id):
    global data
    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)
    acct = user_from_token(token)
    
    # raise AccessError if authorised user not in channel
    if (channel_id in acct.in_channel) == False:
        raise AccessError('authorised user is not in channel')

    for j in data['channels'][index].members:
        if j == acct.u_id:
            data['channels'][index].members.remove(j) #DONT use .pop as it takes in the index, .remove takes in element
    
    for j in data['channels'][index].owners:
        if j == acct.u_id:
            data['channels'][index].owners.remove(j)

    #TODO: Add admin attribute to class in class_defines.py
    #for j in data['channels'][index].admins:
    #    if j == acct.u_id:
    #        data['channels'][index].admins.remove(j)

    return {
    }

# def test_channel_leave():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail2@gmail.com", "password123456", "John2", "Smith2"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad2@gmail.com", "password142256", "Emad2", "Siddiqui2"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']

#     auth_register_dict3 = json.loads(auth_register("email2@gmail.com", "password13456", "Firstname2", "Lastname2"))
#     uid3 = auth_register_dict3['u_id']

#     channel_dict = channels_create(token, "tokenchannel2", False) # create PRIVATE token's channel
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_leave(token, 00000000000) #ValueError since channel_id does not exist

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_leave(token2, channel_id) # token2 is not a part of channel_id, AccessError

#     channel_invite(token, channel_id, uid2) # add token2 to channel
#     # assert that uid2 has been added
#     assert json.loads(channel_details(token, channel_id))['members'] == [uid, uid2]

#     channel_leave(token2, channel_id) # should work as now token2 is part of channel
#     # assert that uid2 has been deleted
#     assert json.loads(channel_details(token, channel_id))['members'] == [uid] 

def channel_add_owner(token, channel_id, u_id):
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # check if user with u_id is already owner 
    if user_from_uid(u_id).u_id in data['channels'][index].owners:
        raise ValueError(description = 'User with u_id is already an owner')

    # check if authorised user is an owner of this channel
    if user_from_token(token).u_id not in data['channels'][index].owners:
        raise AccessError(description = 'Authorised user not an owner of this channel')
    
    data['channels'][index].owners.append(u_id)

    return {
    }

# def test_channel_add_owner():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail3@gmail.com", "password123456", "John3", "Smith3"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad3@gmail.com", "password142256", "Emad3", "Siddiqui3"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']

#     auth_register_dict3 = json.loads(auth_register("email3@gmail.com", "password13456", "Firstname3", "Lastname3"))
#     uid3 = auth_register_dict3['u_id']

#     channel_dict = channels_create(token, "tokenchannel3", False) # create PRIVATE token's channel
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_add_owner(token, 00000000000, uid2) #ValueError since channel_id does not exist

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_add_owner(token, channel_id, uid) # ValueError, u_id is already an owner
    
#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_add_owner(token2, channel_id, uid3) # AccessError token2 is not an owner of slackr or channel
    
#     channel_add_owner(token, channel_id, uid2) # make token2 an owner
#     assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]
#     channel_add_owner(token2, channel_id, uid3) # Exception should now not be raised
#     assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2, uid3]

def channel_remove_owner(token, channel_id, u_id):
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise ValueError if u_id is not an owner
    if u_id not in data['channels'][index].owners:
        raise ValueError(description = 'u_id is not an owner of the channel')

    # raise AccessError if token is not an owner of this channel
    if user_from_token(token).u_id not in data['channels'][index].owners:
        raise AccessError(description = 'authorised user is not an owner of this channel')
    
    data['channels'][index].owners.remove(u_id)

    return {
    }

# def test_channel_remove_owner():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail4@gmail.com", "password123456", "John4", "Smith4"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad4@gmail.com", "password142256", "Emad4", "Siddiqui4"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']

#     auth_register_dict3 = json.loads(auth_register("email4@gmail.com", "password13456", "Firstname4", "Lastname4"))
#     uid3 = auth_register_dict3['u_id']

#     channel_dict = channels_create(token, "tokenchannel4", True)
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_remove_owner(token, 00000000000, uid2) # ValueError since channel_id does not exist

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_remove_owner(token2, channel_id, uid3) # AccessError since token2 is not an owner of slackr or channel

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_remove_owner(token, channel_id, uid2) # ValueError since uid2 is not an owner
    
#     channel_add_owner(token, channel_id, uid2) # make uid2 an owner
#     assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]
#     channel_remove_owner(token, channel_id, uid2) # Exception should now not be raised
#     assert json.loads(channel_details(token, channel_id))['owners'] == [uid]


def channel_details(token, channel_id):
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError('authorised user is not in channel')
    acct = user_from_token(token)
    if (channel_id in acct.in_channel) == False:
        raise AccessError(description = 'authorised user is not in channel')

    channel_name = data['channels'][index].name

    owners_uid = []
    members_uid = []

    for i in data['channels'][index].owners:
        owners_uid.append(i)
    
    for i in data['channels'][index].members:
       members_uid.append(i)
    
    return {
        'name': channel_name,
        'owners': owners_uid,
        'members': members_uid
    }

# def test_channel_details():
#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail5@gmail.com", "password123456", "John5", "Smith5"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad5@gmail.com", "password142256", "Emad5", "Siddiqui5"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']

#     channel_dict = channels_create(token, "tokenchannel5", True)
#     channel_id = channel_dict['channel_id']
#     #SETUP END

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_details(token, 000000) # ValueError since channel_id does not exist

#     with pytest.raises(Exception): # Following should raise exceptions
#         channel_details(token2, channel_id) # AccessError since token2 is not in channel
    
#     # channel_details has been further tested in the asserts of other test functions, 
#     # such as assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]

def channels_list(token):
    global data

    # testing set up
    #data['channels'][0].members.append(user_from_token(token))
    # testing set up

    channel_list = []
    for channel in data['channels']:
        for u_id in channel.members:
            if u_id == user_from_token(token).u_id:
                list_dict = {'channel_id':channel.channel_id, 'name':channel.name}
                channel_list.append(list_dict)
    print(channel_list)
    return {
        'channels': channel_list
    }

# def test_channels_list():
#     # empty data['channels'] & ['accounts'] since it may be populated from other tests
#     data['channels'].clear
#     data['accounts'].clear

#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail6@gmail.com", "password123456", "John6", "Smith6"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad6@gmail.com", "password142256", "Emad6", "Siddiqui6"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']
#     #SETUP END

#     channel_dict = channels_create(token, "tokenchannel6", True) # token1's channel
#     channel_id = channel_dict['channel_id']
    
#     channel_dict2 = channels_create(token2, "token2channel6", True) # token2's channel
#     channel_id2 = channel_dict2['channel_id']

#     list_dict = channels_list(token) # should work
#     assert channels_list(token)['channels'] == [{'channel_id':channel_id, 'name':"tokenchannel6"}] # displays token1's channel only
#     assert channels_list(token2)['channels'] == [{'channel_id':channel_id2, 'name':"token2channel6"}] # displays token2's channel only

def channels_listall(token):
    global data

    channel_list = []
    for channel in data['channels']:
        list_dict = {'channel_id': channel.channel_id, 'name': channel.name}
        channel_list.append(list_dict)

    return {
        'channels': channel_list
    }

# def test_channels_listall():
#     # empty data['channels'] & ['accounts'] since it may be populated from other tests
#     data['channels'].clear
#     data['accounts'].clear

#     #SETUP START
#     auth_register_dict = json.loads(auth_register("goodemail7@gmail.com", "password123456", "John7", "Smith7"))
#     token = auth_register_dict['token']
#     uid = auth_register_dict['u_id']

#     auth_register_dict2 = json.loads(auth_register("emad7@gmail.com", "password142256", "Emad7", "Siddiqui7"))
#     token2 = auth_register_dict2['token']
#     uid2 = auth_register_dict2['u_id']
#     #SETUP END
#     channel_dict = channels_create(token, "tokenchannel7", True) # token1's channel
#     channel_id = channel_dict['channel_id']

#     #assert json.loads(channels_listall(token))['channels'] == [{'channel_id':channel_id, 'name':"tokenchannel6"}] # displays token1's channel only

#     channel_dict2 = channels_create(token2, "token2channel", True) # token1's channel
#     channel_id = channel_dict2['channel_id']

def channel_messages(token, channel_id, start):
    global data

    # raise ValueError if channel_id doesn't exist (channel_index)
    index = channel_index(channel_id)

    # raise AccessError if authorised user isn't in channel
    if user_from_token(token).u_id not in data['channels'][index].members:
        raise AccessError(description = 'authorised user is not in channel')

    # raise ValueError if start is greater than no. of total messages
    no_total_messages = len(data['channels'][index].messages)
    if start > no_total_messages:
        raise ValueError(description = 'start is greater than no. of total messages')
    
    # { message_id, u_id, message, time_created, reacts, is_pinned,  }
    end = -1
    list_messages = []
    i = start
    # index50 = start + 50
    # index50 <= no_total_messages, end = index50
    #print(data['channels'][index].messages)

    for item in data['channels'][index].messages[i:]:
        #print(item)
        message = {}
        message['message_id'] = item.message_id
        message['u_id'] = item.sender
        message['message'] = item.message
        message['time_created'] = item.create_time
        message['reacts'] = item.reaction
        message['is_pinned'] = item.is_pinned

        i = i + 1
        list_messages.append(message)
        if i == no_total_messages:
            end = -1
            break
        if i == (start + 50):
            end = i
            break
    
    return {
        'messages': list_messages,
        'start': start,
        'end': end
    }

def test_channel_messages():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail7@gmail.com", "password123456", "John7", "Smith7"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad7@gmail.com", "password142256", "Emad7", "Siddiqui7"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']
    #SETUP END
    channel_dict = channels_create(token, "tokenchannel7", True) # token1's channel
    channel_id = channel_dict['channel_id']

    msg_send(token, "2Hi, this is a message.", channel_id)
    msg_send(token, "3Hi, this is a message.", channel_id)
    msg_send(token, "4Hi, this is a message.", channel_id)
    msg_send(token, "5Hi, this is a message.", channel_id)
    i = 0
    while i < 60:
        msg_send(token, "Hi, this is a message.", channel_id)
        i = i + 1

    print(channel_messages(token, channel_id, 0))
    assert False==True


if __name__ == '__main__':
    app.run(port = 5022, debug=True)
