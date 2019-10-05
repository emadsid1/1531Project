from Error import AccessError
from datetime import datetime
import pytest

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
        channel_join(token, channel_id + 100)

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

    channels_create_dict = channels_create(token, "User 1's created Channel", False)
    channel_id = channels_create_dict['channel_id']

    with pytest.raises(AccessError):
        channel_addowner(token, channel_id, u_id2)  # fail since u_id2 (token2) has no access to the channel
        channel_addowner(token2, channel_id, u_id2) # as channel was created by u_id (token)
                                                    

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

    channels_create_dict = channels_create(token, "User 1's created Channel", False)
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

def channels_create_test()
    assert channels_create('valid token', 'Jeffrey', True) == 12345
    with pytest.raises(Exception): # Following should raise exceptions
        assert channels_create('valid token', 'This is a string that is much longer than the max length', True)

def user_profile_setname_test():
    #user_profile_setname(token, firstname, lastname), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #SETUP TESTS END
    user_profile_setname(token, "Jeffrey", "Oh")
    with pytest.raises(Exception): #ValueError, match=r"*"
        user_profile_setname(token, "This is a really long first name, more than 50 characters", "lmao")
        user_profile_setname(token, "lmao", "This is a really long last name, more than 50 characters")
        user_profile_setname(token, "This is a really long first name, more than 50 characters", "This is a really long last name, more than 50 characters")
        #TODO: does there need to be a test with an incorrect token?

def user_profile_setemail_test():
    #user_profile_setemail(token, email), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #create second person's email:
    authRegDict2 = auth_register("jeffrey.oh@student.unsw.edu.au", "password", "Jeffrey", "Oh")
    userDict2 = user_profile(authRegDict2["u_id"], authRegDict2["token"])
    email2 = userDict2["email"]
    #SETUP TESTS END
    user_profile_setemail(token, "goodemail@student.unsw.edu.au")
    with pytest.raises(Exception): #ValueError, match=r"*""
        user_profile_setemail(token, "bad email")
        user_profile_setemail(token, email2)

def user_profile_sethandle_test():
    #user_profile_sethandle(token, handle_str), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #SETUP TESTS END
    user_profile_sethandle(token, "good handle")
    with pytest.raises(Exception):
        user_profile_sethandle(token, "This handle is way too long")

def user_profiles_uploadphoto_test():
    #user_profile_sethandle(token, img_url, x_start, y_start, x_end, y_end), no return value
    #SETUP TESTS BEGIN
    #create token:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #SETUP TESTS END
    user_profiles_uploadphoto(token, "exampleimage.jpg", 100, 100, 200, 200)
    #TODO: wtf are image urls and their sizes, and how do you get a http status

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
    #create channel
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    #SETUP TESTS END
    standup_send(token, chanId, "Standup message")
    with pytest.raises(Exception):
        assert standup_send(token, 55555555, "Standup message with wrong chanId")
        assert standup_send(token, chanId, '''Standup message longer than 1000 chars''')
        assert standup_send(token2, chanId, "Standup message with user not a member of the channel")
        assert standup_send() '''the standup time is finished'''
    #TODO: figure out a message that is longer than 1000 chars, and how to represent standup time

def search_test():
    #search(token, query_str), returns messages
    #SETUP TESTS BEGIN
    #create new users:
    authRegDict = auth_register("benjamin.kah@student.unsw.edu.au", "password", "Ben", "Kah")
    token = authRegDict["token"]
    #create channel
    chanCreateDict = channels_create(token, "test channel", True)
    chanId = chanCreateDict["channel_id"]
    #create message
    message_send(token, chanId, "New message sent")
    #SETUP TESTS END
    search(token, "message")

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
    #add regular user to channel:
    channel_invite(token, chanId, userId2)
    #SETUP TESTS END
    #regular user is promoted
    admin_userpermission_change(token, userId2, 1)
    admin_userpermission_change(token, userId2, 2)
    #regular user is demoted
    admin_userpermission_change(token, userId2, 3)
    with pytest.raises(Exception):
        assert admin_userpermission_change(token2, userId, 3)
        assert admin_userpermission_change(token, userId, 0)
        assert admin_userpermission_change(token, userId, 4)
        assert admin_userpermission_change(token, 55555, 3)
