import pytest
import functions
from Error import AccessError
from datetime import datetime, timedelta


def auth_login_test():
    assert auth_login('z5555555@student.unsw.edu.au', 'right password') == (12345, 'correct token')
    with pytest.raises(ValueError): # Following should raise exceptions
        assert auth_login('bad email', 'right password')
        assert auth_login('z5555555@asdfghjkl', 'right password')
        assert auth_login('z55555@.com', 'right password')
        assert auth_login('@', 'right password')
        assert auth_login('.com', 'right password')
        assert auth_login('z5555555@student.unsw.edu.au', 'wrong password')
        assert auth_login('z5555555@asdfghjkl', 'wrong password')

def auth_logout_test():
    auth_logout('Active token') # Should log out user
    auth_logout('Inactive token')   # Should do nothing

def auth_register_test():
    assert auth_register('jeffrey.oh@student.unsw.edu.au', 'right password', 'Jeffrey', 'Oh') == ('12345', 'correct token')
    with pytest.raises(ValueError): # Following should raise exceptions
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good     password', 'Jeffrey', 'This is a string that is much longer than the max length')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good password', 'This is a string that is much longer than the max length', 'Oh')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'password that does not meet requirements', 'Jeffrey', 'Oh')
        assert auth_register('bad email', 'good password', 'Jeffrey', 'Oh')

def auth_passwordreset_request_test():
    auth_passwordreset_request('Registered email')  # Should send reset requesy
    auth_passwordreset_request('Unregistered email')    # Should do nothing

def auth_passwordreset_reset_test():
    auth_passwordreset_reset('Valid reset code', 'Valid password')    # No exception raised
    with pytest.raises(ValueError):   # Following should raise exceptions
        auth_passwordreset_reset('Invalid reset code', 'Valid password')
        auth_passwordreset_reset('Valid reset code', 'Invalid password')
        auth_passwordreset_reset('Invalid reset code', 'Invalid password')

def channel_invite_test():
    channel_invite('Token', 1, 1)   # Valid u_id, valid channel_id
    with pytest.raises(ValueError):
        channel_invite('Token', 12345, 12345)   # Invalid u_id, invalid channel_id

def channel_details_test():
    assert channel_details('Valid token', 123) == ('Owner name', list_of_owner_members, list_of_all_members)
    with pytest.raises(ValueError):  # Following should raise exceptions
        channel_details('Valid token', 123) # If channel 123 does not exist
    with pytest.raises(AccessError):  # Following should raise exceptions
        channel_details('Invalid token', 123)   # User is not in the channel



def channel_messages_test():
    assert channel_messages('Valid token', 1, 1) == (valid_messages, 1, 5) # Assuming all inputs are valid, outputs desired messages with correct start and end
    with pytest.raises(ValueError):  # Following should raise exceptions
        channel_messages('Valid token', 123, 123)   # Channel id does not exist
        channel_messages('Valid token', 123, 123)   # Start exceeeds number of messages
    with pytest.raises(AccessError):  # Following should raise exceptions
        channel_messages('Invalid token', 1, 1) # User token is not in channel


def channel_leave_test():
    # Token
    auth_register_dict = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    token = auth_register_dict('token')

    auth_register_dict2 = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    token2 = auth_register_dict2('token')

    # Channel ID
    channels_create_dict = channels_create(token, "Channel 1", True)
    channel_id = channels_create_dict('channel_id')

    channels_create_dict2 = channels_create(token2, "Channel 2", False) #assumes token2 has access to the Private channel***
    channel_id2 = channels_create_dict2('channel_id')

    # leaving a public channel 1
    channel_leave(token, channel_id)
    # leaving a private channel 2
    channel_leave(token2, channel_id2)

    with pytest.raises(ValueError):
        # channel does not exist (channel id doesn't correspond to a created channel)
        channel_leave(token, channel_id + 100)
        # trying to leave a channel you were not a part of in the first place
        # ex. John tries to leave Channel 2, when he is part of Channel 1
        channel_leave(token, channel_id2)

def channel_join_test():
    # Token
    auth_register_dict = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    token = auth_register_dict('token')

    auth_register_dict2 = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    token2 = auth_register_dict2('token')

    # Channel ID
    channels_create_dict = channels_create(token, "Channel 1", True)
    channel_id = channels_create_dict('channel_id')

    channels_create_dict2 = channels_create(token2, "Channel 2", False)
    channel_id2 = channels_create_dict2('channel_id')

    # channel_join(token, channel_id)
    channel_join(token, channel_id)

    with pytest.raises(Value
    # TODO not sure what the messaes data type isges data type isError):
        # channel does not exist (channel id doesn't correspond to a created channel)
        #channel_join(token, channel_id + 100)

    with pytest.raises(AccessError):
        # channel is private & user is not admin
        channel_join(token, channel_id2)

def channel_addowner_test():
    # user 1
    auth_register_dict = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    u_id = auth_register_dict['u_id']
    token = auth_register_dict['token']
    # user 2
    auth_register_dict2 = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    u_id2 = auth_register_dict2('u_id')
    token2 = auth_register_dict2('token')

    channels_create_dict = channels_create(token, "User 1's created Channel", True)
    channel_id = channels_create_dict['channel_id']

    with pytest.raises(AccessError):
        channel_addowner(token, channel_id, u_id2)  # fail since u_id2 (token2) has no access to the channel
        channel_addowner(token2, channel_id, u_id2) # as channel was created by u_id (token)

    # u_id2 needs to be a member of the channel to be made an owner **assumption
    channel_join(token2, channel_id)
    channel_addowner(token, channel_id, u_id2) # works as u_id2 isn't owner
    with pytest.raises(ValueError):
        channel_addowner(token, channel_id, u_id) # fail since u_id created channel & thus already is owner
        channel_addowner(token, channel_id, u_id2) # fail since u_id2 has already been made owner previously
        channel_addowner(token, channel_id + 1, u_id2) # fail since channel does not exist

def channel_removeowner_test():
    # user 1
    auth_register_dict = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    u_id = auth_register_dict['u_id']
    token = auth_register_dict['token']
    # user 2
    auth_register_dict2 = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    u_id2 = auth_register_dict2('u_id')
    token2 = auth_register_dict2('token')

    channels_create_dict = channels_create(token, "User 1's created Channel", True)
    channel_id = channels_create_dict['channel_id']

    with pytest.raises(ValueError):
        channel_removeowner(token, channel_id, u_id2) # fail since u_id2 is not an owner
        channel_removeowner(token, channel_id + 1, u_id) # fail since channel ID is incorrect

    with pytest.raises(AccessError):
        channel_removeowner(token2, channel_id, u_id) # fail since u_id2 (token2) has no access to the channel
        channel_removeowner(token, channel_id, u_id2) # as channel was created by u_id (token)

        #what happens when you remove the owner from a channel which has only 1 owner?
        channel_removeowner(token, channel_id, u_id) # fail since you cannot remove the sole owner of a channel ***assumption

    # this should work as there will still be an owner of the channel
    channel_addowner(token, channel_id, u_id2) # add u_id2 as owner
    channel_removeowner(token, channel_id, u_id) # remove u_id from being owner

# to better justify the purpose of these two different listing functions, channels_list will ONLY list functions the auth user is part of
# and channels_listall will list functions the auth user is part of in addition to ALL public channels available (regardless of membership).
def channels_list_test():
    # assume that this function displays ALL channels that the authorised user is part of**

    # user 1
    auth_register_dict = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    u_id = auth_register_dict['u_id']
    token = auth_register_dict['token']
    # user 2
    auth_register_dict2 = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    u_id2 = auth_register_dict2('u_id')
    token2 = auth_register_dict2('token')

    channels_create_dict = channels_create(token, "User 1's private channel", False)
    channel_id = channels_create_dict['channel_id']

    channels_create_dict2 = channels_create(token2, "User 2's public channel", True)
    channel_id2 = channels_create_dict2['channel_id']

    # lists channels that only the authorised user is part of
    assert channels_list(token) = ["User 1's private channel"]
    assert channels_list(token2) = ["User 2's public channel"] # user 2 doesn't list user 1's private channel

    # add user 1 to user 2's channel and list user 1's channels
    channel_join(token, channel_id2) # user 1 can join as channel_id2 is public
    assert channels_list(token) = ["User 1's private channel", "User 2's public channel"]

def channels_listall_test():
    # assume channels_listall will list functions the auth user is part of in addition to ALL public channels available (regardless of membership).**
    # user 1
    auth_register_dict = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    u_id = auth_register_dict['u_id']
    token = auth_register_dict['token']
    # user 2
    auth_register_dict2 = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    u_id2 = auth_register_dict2('u_id')
    token2 = auth_register_dict2('token')

    channels_create_dict = channels_create(token, "User 1's private channel", False)
    channel_id = channels_create_dict['channel_id']

    channels_create_dict2 = channels_create(token2, "User 2's public channel", True)
    channel_id2 = channels_create_dict2['channel_id']

    channels_create_dict3 = channels_create(token2, "User 2's second public channel", True)
    channel_id3 = channels_create_dict3['channel_id']

    # lists channels token is a part of AND all public channels available
    # lists user 1's private channel and all public channels despite not being a part of them
    assert channels_listall(token) = ["User 1's private channel", "User 2's public channel", "User 2's second public channel"]
    # lists all user 2's channels but not user 1's  channel since it is private
    assert channels_listall(token2) = ["User 2's public channel", "User 2's second public channel"] #assume channel order in list doesn't matter ***

def channels_create_test()
    assert channels_create('valid token', 'Jeffrey', True) == 12345
    with pytest.raises(Exception): # Following should raise exceptions
        assert channels_create('valid token', 'This is a string that is much longer than the max length', True)

def message_sendlater_test():
    auth_register_dict = auth_register("emad@gmail.com", "123456", "Emad", "Siddiqui")
    u_id = auth_register_dict['u_id']
    token = auth_register_dict['token']

    channels_create_dict = channels_create(token, "Channel 1", False)
    channel_id = channels_create_dict['channel_id']

    morethan1000characters = "a" * 1001
    exactly1000characters = "a" * 1000
    future_time = datetime.max
    past_time = datetime.min

    message_sendlater(token, channel_id, exactly1000characters, future_time) # should work since 1000 characters (testing >=)

    with pytest.raises(ValueError):
        message_sendlater(token, channel_id, morethan1000characters, future_time) # fail since message is more than 1000 characters
        message_sendlater(token, channel_id, "", future_time) # fail since blank
        message_sendlater(token, channel_id, exactly1000characters, past_time) # fail since time sent is in past
        message_sendlater(token, channel_id + 1, exactly1000characters, past_time) # fail since channel ID is incorrect

    #raise Access error if UNauthorised user tries to send message
    # user 2
    auth_register_dict2 = auth_register("goodemail@gmail.com", "123456", "John", "Smith")
    u_id2 = auth_register_dict2('u_id')
    token2 = auth_register_dict2('token')
    with pytest.raises(AccessError):
        message_sendlater(token2, channel_id, exactly1000characters, future_time) # fail since token2 is not authorised

def message_send_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "123456", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # channel created by user1
    channelDict = channels_create(token1, "kenny's channel", True)
    channelID = channelDict['channel_id']
    # two long sentances with more than 1000 characters
    long_sentance = "a" * 1001
    # end of set up

    # testing
    # raises AccessError if unauthorised user tries to send message
    with pytest.raises(AccessError, ):
        message_send(token2, channelID, "This is from Ken")
    # raises ValueError if the message is more than 1000 characters but exact 1000 characters is fine
    with pytest.raises(ValueError):
        message_send(token1, channelID, long_sentance)
    # tesing end

def message_remove_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # user3
    registerDict3 = auth_register("k@gmail.com", "666666", "k", "h")
    userID3 = registerDict3['u_id']
    token3 = registerDict3['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageUserID1 = messageList[0]['u_id']
    # end of set up

    # testing
    # raises AccessError when message with message_id was not sent by the authorised user making this request
    with pytest.raises(AccessError):
        message_remove(token3, messageID1)
    # raises AccessError when message with message_id was not sent by an owner of this channel or admin of slackr
    with pytest.raises(AccessError):
        message_remove(token2, messageID1)
    # raises ValueError when message(based on ID) no longer exists
    message_remove(token1, messageID1)
    with pytest.raises(ValueError):
        message_remove(token1, messageID1)
    # end of testing

def message_edit_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # user3
    registerDict3 = auth_register("k@gmail.com", "666666", "k", "h")
    userID3 = registerDict3['u_id']
    token3 = registerDict3['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 is the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    message_send(token3, channelID1, "Yo")
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageID2 = messageList[1]['message_id']
    # end of set up

    # testing, AccessError here is better?
    # raises ValueError when message with message_id was not sent by the authorised user making this request
    with pytest.raises(ValueError):
        message_edit(token3, messageID1)
    # raises ValueError when message with message_id was not sent by an owner of this channel or admin of slackr
    with pytest.raises(ValueError):
        message_edit(token2, messageID2)
    # end of testing

def message_react_test():
    # set up
    rections = {'thumb_up': 1, 'thumb_down': 2, 'happy': 3, 'angry': 4}
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 is the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_invite(token2, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageID2 = messageList[1]['message_id']
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message within a channel that the authorised user has joined
    with pytest.raises(ValueError):
        message_react(token1, messageID2, rections['happy'])
    with pytest.raises(ValueError):
        message_react(token1, "@#$%^&*!", rections['happy'])
    # raises ValueError when react_id is not a valid React ID, assuming there are only 4 reactions
    with pytest.raises(ValueError):
        message_react(token1, messageID1, rections['not_happy'])
    # raises ValueError when message with ID message_id already contains an active React with ID react_id
    message_react(token1, messageID1, rections['happy'])
    with pytest.raises(ValueError):
        message_react(token1, messageID1, rections['angry'])
    # end of testing

def message_unreact_test():
    # set up
    # assume there are only 4 reactions
    rections = {'thumb_up': 1, 'thumb_down': 2, 'happy': 3, 'angry': 4}
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 is the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_invite(token2, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageID2 = messageList[1]['message_id']
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message within a channel that the authorised user has joined
    with pytest.raises(ValueError):
        message_unreact(token1, messageID2, rections['happy'])
    with pytest.raises(ValueError):
        message_unreact(token1, "@#$%^&*!", rections['happy'])
    # raises ValueError when react_id is not a valid React ID, assuming there are only 4 reactions
    with pytest.raises(ValueError):
        message_unreact(token1, messageID1, rections['not_happy'])
    # raises ValueError when message with ID message_id does not contain an active React with ID react_id
    message_react(token1, messageID1, rections['happy'])
    message_unreact(token1, messageID1, rections['happy'])
    with pytest.raises(ValueError):
        message_unreact(token1, messageID1, rections['happy'])
    # end of testing

def message_pin_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    token2 = registerDict2['token']
    # user3
    registerDict3 = auth_register("k@gmail.com", "666666", "k", "h")
    token3 = registerDict3['token']
    # user4
    registerDict4 = auth_register("user4@gmail.com", "212121", "user4", "ha")
    userID4 = registerDict4['u_id']
    token4 = registerDict4['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    message_send(token3, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageUserID1 = messageList[0]['u_id']
    messageID3 = messageList[2]['message_id']
    messageUserID3 = messageList[2]['u_id']
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message
    with pytest.raises(ValueError):
        message_pin(token3, messageID3)
    with pytest.raises(ValueError):
        message_pin(token1, "@#$%^&*!")
    # raises Value Error when the authorised user is not an admin
    with pytest.raises(ValueError):
        message_pin(token2, messageUserID1)
    # raises AccessError when the authorised user is not a member of the channel that the message is within
    with pytest.raises(AccessError):
        message_pin(token4, messageID1)
    # raises ValueError when message with ID message_id is already pinned
    message_pin(token1, messageID1)
    with pytest.raises(ValueError):
        message_pin(token1, messageID1)
    # end of testing

def message_unpin_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    token2 = registerDict2['token']
    # user3
    registerDict3 = auth_register("k@gmail.com", "666666", "k", "h")
    token3 = registerDict3['token']
    # user4
    registerDict4 = auth_register("user4@gmail.com", "212121", "user4", "ha")
    userID4 = registerDict4['u_id']
    token4 = registerDict4['token']
    # channel created by user1
    channelDict1 = channels_create(token1, "kenny's channel", True)
    channelID1 = channelDict1['channel_id']
    # make sure user1 the admin
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    message_send(token3, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages
    messageID1 = messageList[0]['message_id']
    messageUserID1 = messageList[0]['u_id']
    messageID3 = messageList[2]['message_id']
    messageUserID3 = messageList[2]['u_id']
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message
    with pytest.raises(ValueError):
        message_unpin(token3, messageID3)
    with pytest.raises(ValueError):
        message_unpin(token1, "@#$%^&*!")
    # raises Value Error when the authorised user is not an admin
    with pytest.raises(ValueError):
        message_unpin(token2, messageUserID1)
    # raises AccessError when the authorised user is not a member of the channel that the message is within
    with pytest.raises(AccessError):
        message_unpin(token4, messageID1)
    # raises ValueError when message with ID message_id is already unpinned
    message_pin(token1, messageID1)
    message_unpin(token1, messageID1)
    with pytest.raises(ValueError):
        message_unpin(token1, messageID1)
    # end of testing

def user_profile_test():
    # set up
    # user1(admin)
    registerDict1 = auth_register("kenny@gmail.com", "123456", "kenny", "han")
    userID1 = registerDict1['u_id']
    token1 = registerDict1['token']
    # user2
    registerDict2 = auth_register("ken@gmail.com", "654321", "ken", "han")
    userID2 = registerDict2['u_id']
    token2 = registerDict2['token']
    # end of set up

    # testing
    # raises ValueError when user with u_id is not a valid user
    with pytest.raises(ValueError):
        userProfile = user_profile(token1, userID2)
    with pytest.raises(ValueError):
        userProfile = user_profile(token2, userID1)
    with pytest,raises(ValueError):
        userProfile = user_profile(token1, "@#$%^&*!")

def user_profile_setname_test():
    #user_profile_setname(token, firstname, lastname), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    userId = authRegDict["u_id"]
    token = authRegDict["token"]
    #SETUP TESTS END
    user_profile_setname(token, "Jeffrey", "Oh") #this function should pass
    userDict = user_profile(token, userId)
    assert userDict["name_first"] == "Jeffrey" #test that name has been changed
    assert userDict["name_last"] == "Oh"
    with pytest.raises(ValueError): #following should raise exceptions
        user_profile_setname(token, "This is a really long first name, more than 50 characters", "lmao")
        user_profile_setname(token, "lmao", "This is a really long last name, more than 50 characters")
        user_profile_setname(token, "This is a really long first name, more than 50 characters", "This is a really long last name, more than 50 characters")

def user_profile_setemail_test():
    #user_profile_setemail(token, email), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    userId = authRegDict["u_id"]
    token = authRegDict["token"]
    #create second person's email:
    authRegDict2 = auth_register("jeffrey.oh@student.unsw.edu.au", "password", "Jeffrey", "Oh")
    userDict2 = user_profile(authRegDict2["token"], authRegDict2["u_id"])
    email2 = userDict2["email"]
    #SETUP TESTS END
    user_profile_setemail(token, "goodemail@student.unsw.edu.au") #this function should pass
    userDict = user_profile(token, userId)
    assert userDict["email"] == "goodemail@student.unsw.edu.au" #test that email has been changed
    with pytest.raises(ValueError): #following should raise exceptions
        user_profile_setemail(token, "bad email")
        user_profile_setemail(token, email2) #using another user's email

def user_profile_sethandle_test():
    #user_profile_sethandle(token, handle_str), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    userId = authRegDict["u_id"]
    token = authRegDict["token"]
    #SETUP TESTS END
    user_profile_sethandle(token, "good handle")
    userDict = user_profile(token, userId)
    assert userDict["handle_str"] == "good handle"
    with pytest.raises(ValueError):
        user_profile_sethandle(token, "This handle is way too long")

def user_profiles_uploadphoto_test():
    #user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #SETUP TESTS END
    assert user_profiles_uploadphoto(token, "http://test_url.com/example.html", 0, 0, 1024, 1024)
    with pytest.raises(ValueError:
        assert user_profiles_uploadphoto(token, "http://test_url.com/negativeexample.html", -1, 0, 1024, 1024)
        assert user_profiles_uploadphoto(token, "http://test_url.com/negativeexample2.html", 0, -1, 1024, 1024)
        assert user_profiles_uploadphoto(token, "http://test_url.com/startgreaterthanendx.html", 1000, 0, 900, 1024)
        assert user_profiles_uploadphoto(token, "http://test_url.com/startgreaterthanendy.html", 0, 1000, 1024, 900)

def standup_start_test():
    #standup_start(token, channel_id), returns time_finish
    #SETUP TESTS BEGIN
    #create new users:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    authRegDict2 = auth_register("jeffrey.oh@student.unsw.edu.au", "password", "Jeffrey", "Oh")
    token2 = authRegDict2["token"]
    #create channel
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    #SETUP TESTS END
    assert standup_start(token, chanId) == '''some time'''
    with pytest.raises(Exception):
        assert standup_start(token, 55555555)
        assert standup_start(token2, chanId)
    #TODO: figure out how to test the time

def standup_send_test():
    #standup_send(token, channel_id, message), no return value
    #SETUP TESTS BEGIN
    #create new users:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    authRegDict2 = auth_register("jeffrey.oh@student.unsw.edu.au", "password", "Jeffrey", "Oh")
    token2 = authRegDict2["token"]
    #create channels:
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    chanCreateDict2 = channels_create(token, "test channel 2", True)
    chanId2 = chanCreateDict2["channel_id"]
    #SETUP TESTS END
    with pytest.raises(AccessError):
        assert standup_send(toke, ChanId, "this is sent before standup_start is called")
    #create time_finish
    standupEnd = standup_start(token, chanId)
    minBefStandupEnd = standupEnd - timedelta(minute = 1)
    minAftStandupEnd = standupEnd + timedelta(minute = 1)
    #this message should be sent, as it will be sent after the standup
    message_sendlater(token, chanId, "this is sent after standup", minAftStandupEnd)
    with pytest.raises(AccessError):
        assert message_send(token, chanId, "this message can't be sent in a standup!")
        assert message_sendlater(token, chanId, "wait until after standup", minBefStandupEnd)
    standup_send(token, chanId, "Standup message")
    with pytest.raises(AccessError):
        assert standup_send(token2, chanId, "Standup message with user not a member of the channel")
    strOver1000 = "yeah bo" + "i"*1000
    with pytest.raises(ValueError):
        assert standup_send(token, chanId, strOver1000)
        assert standup_send(token, chanId2, "Standup message with wrong chanId")
    #TODO: how to represent standup time

def search_test():
    #search(token, query_str), returns messages
    #SETUP TESTS BEGIN
    #create new users:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #create channel
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    #create messages
    message_send(token, chanId, "New message sent")
    message_send(token, chanId, "Another message")
    message_send(token, chanId, "A completely different string")
    #SETUP TESTS END
    searchResultsList = search(token, "message") #first search query
    searchResultsList2 = search(token, "nothing to find") #second search query
    assert searchResultsList[0]["message"] == "New message sent" #search results should contain these strings
    assert searchResultsList[1]["message"] == "Another message"
    assert len(searchResultsList) == 2
    assert searchResultsList2 == False #list should be empty

def admin_userpermission_change_test():
    #admin_userpermission_change(token, u_id, permission_id), no return value
    #SETUP TESTS BEGIN
    #create new admin:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    userId = authRegDict["u_id"]
    #create regular user:
    authRegDict2 = auth_register("jeffrey.oh@student.unsw.edu.au", "password", "Jeffrey", "Oh")
    token2 = authRegDict2["token"]
    userId2 = authRegDict2["u_id"]
    #create channel from admin:
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    #add regular user to first channel:
    channel_invite(token, chanId, userId2)
    #SETUP TESTS END
    admin_userpermission_change(token, userId2, 3) #confirm regular user is a member
    with pytest.raises(AccessError):
        assert channel_removeowner(token2, chanId, userId) #regular user should not have permission to do this

    admin_userpermission_change(token, userId2, 1) #make regular user an owner
    channel_removeowner(token2, chanId, userId) #revoke original admin's permissions - should pass

    admin_userpermission_change(token2, userId, 2) #make original admin an admin again
    channel_removeowner(token, chanId, userId2) #original admin removes new owner's privileges - should pass

    admin_userpermission_change(token, userId2, 1) #add regular user as an owner again to set up next test
    #create second channel:
    chanCreateDict2 = channels_create(token, "test channel 2", True)
    chanId2 = chanCreateDict2["channel_id"]
    #add regular user to second channel:
    channel_invite(token, chanId, userId2) #owner of channel 1 should not be owner of this channel
    with pytest.raises(AccessError):
        assert channel_removeowner(token2, chanId2, userId) #regular user should not have permission to do this

    with pytest.raises(ValueError):
        assert admin_userpermission_change(token, userId, 0) #invalid permission_id
        assert admin_userpermission_change(token, userId, 4)
        assert admin_userpermission_change(token, 55555, 3) #invalid user ID
