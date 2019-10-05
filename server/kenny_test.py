from Error import AccessError
from datetime import datetime
import pytest

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
    long_sentance1 = "a" * 1000
    long_sentance2 = "21" * 1000
    # end of set up

    # testing
    # raises AccessError if unauthorised user tries to send message
    with pytest.raises(AccessError, match=r"*"):
        message_send(token2, channelID, "This is from Ken")
    # raises ValueError if the message is more than 1000 characters but exact 1000 characters is fine
    message_send(token1, channelID, long_sentance1)     # TODO how to test if the function is working fine
    with pytest.raises(ValueError):
        message_send(token1, channelID, long_sentance2)
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
    # make sure user1 the admin TODO not sure if we need to do this 
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    messageDetails = channel_messages(token1, channelID1, 0)
    messageList = messageDetails.messages                       # TODO not sure if this one is right
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
    # make sure user1 is the admin TODO not sure if we need to do this
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_join(token2, channelID1)
    channel_invite(token3, channelID1)
    # message details
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, "Hey")
    message_send(token3, channelID1, "Yo")
    messageDetails = channel_messages(token1, channelID1, 0)    # TODO not sure if this one is right
    messageList = messageDetails.messages                       # TODO not sure if this one is right
    messageID1 = messageList[0]['message_id']                   # TODO not sure if this one is right
    messageID2 = messageList[1]['message_id']                   # TODO not sure if this one is right
    # end of set up

    # testing TODO I think all these should be AccessError
    # raises ValueError when message with message_id was not sent by the authorised user making this request
    with pytest.raises(ValueError):                             
        message_edit(token3, messageID1) 
    # raises ValueError when message with message_id was not sent by an owner of this channel or admin of slackr
    with pytest.raises(ValueError):
        message_edit(token2, messageID2)
    # end of testing

def message_react_test():
    # set up
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
    # make sure user1 is the admin TODO not sure if we need to do this
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_invite(token2, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)    # TODO not sure if this one is right
    messageList = messageDetails.messages                       # TODO not sure if this one is right
    messageID1 = messageList[0]['message_id']                   # TODO not sure if this one is right
    messageID2 = messageList[1]['message_id']                   # TODO not sure if this one is right
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message within a channel that the authorised user has joined
    with pytest.raises(ValueError):
        message_react(token1, messageID2, 1)
    with pytest.raises(ValueError):
        message_react(token1, "@#$%^&*!", 1)
    # raises ValueError when react_id is not a valid React ID
    with pytest.raises(ValueError):
        message_react(token1, messageID1, 5)                    # TODO assuming there are only 4 rections
    # raises ValueError when message with ID message_id already contains an active React with ID react_id
    message_react(token1, messageID1, 1)
    with pytest.raises(ValueError):
        message_react(token1, messageID1, 2)
    # end of testing

def message_unreact_test():
    # set up
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
    # make sure user1 is the admin TODO not sure if we need to do this
    admin_userpermission_change(token1, userID1, 2)
    # user2 is just a member of channel1, user1 and user3 are the owners of channel1
    channel_invite(token2, channelID1)
    # message details
    # create invalid message
    long_sentance = "a" * 1001
    message_send(token1, channelID1, "Hello")
    message_send(token2, channelID1, long_sentance)
    messageDetails = channel_messages(token1, channelID1, 0)    # TODO not sure if this one is right
    messageList = messageDetails.messages                       # TODO not sure if this one is right
    messageID1 = messageList[0]['message_id']                   # TODO not sure if this one is right
    messageID2 = messageList[1]['message_id']                   # TODO not sure if this one is right
    # end of set up

    # testing
    # raises ValueError when message_id is not a valid message within a channel that the authorised user has joined
    with pytest.raises(ValueError):
        message_unreact(token1, messageID2, 1)
    with pytest.raises(ValueError):
        message_unreact(token1, "@#$%^&*!", 1)
    # raises ValueError when react_id is not a valid React ID
    with pytest.raises(ValueError):
        message_unreact(token1, messageID1, 5)                    # TODO assuming there are only 4 rections
    # raises ValueError when message with ID message_id does not contain an active React with ID react_id
    message_react(token1, messageID1, 1)
    message_unreact(token1, messageID1, 1)
    with pytest.raises(ValueError):
        message_unreact(token1, messageID1, 1)
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
    # make sure user1 the admin TODO not sure if we need to do this
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
    messageList = messageDetails.messages                       # TODO not sure if this one is right
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
    # make sure user1 the admin TODO not sure if we need to do this
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
    messageList = messageDetails.messages                       # TODO not sure if this one is right
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


