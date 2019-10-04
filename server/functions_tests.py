from Error import AccessError
import pytest

def auth_login_test():
    # TODO (Fucking apparently we just assume whether the password and email are right or not, and the returned tokens are whatever we want) PLEASE double check tho
    # TODO check if right BUT u_id is some sort of integer and token is a string
    assert auth_login('z5555555@student.unsw.edu.au', 'right password') == (12345, 'correct token')
    with pytest.raises(Exception): # Following should raise exceptions
        assert auth_login('bad email', 'right password')
        assert auth_login('z5555555@asdfghjkl', 'right password')
        assert auth_login('z55555@.com', 'right password')
        assert auth_login('@', 'right password')
        assert auth_login('.com', 'right password')
        assert auth_login('z5555555@student.unsw.edu.au', 'wrong password')
        assert auth_login('z5555555@asdfghjkl', 'wrong password')

def auth_logout_test():
    # TODO if no output how to test?

def auth_register_test():
    assert auth_register('jeffrey.oh@student.unsw.edu.au', 'right password', 'Jeffrey', 'Oh') == ('12345', 'correct token')
    with pytest.raises(Exception): # Following should raise exceptions
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good     password', 'Jeffrey', 'This is a string that is much longer than the max length')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good password', 'This is a string that is much longer than the max length', 'Oh')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'password that does not meet requirements', 'Jeffrey', 'Oh')
        assert auth_register('bad email', 'good password', 'Jeffrey', 'Oh')

def auth_passwordreset_request_test():
    # TODO if no output how to test?

def auth_passwordreset_reset_test():
    # TODO if no output how to test?

def channel_invite_test():
    # TODO if no output how to test?

def channel_details_test():
    assert channel_details('valid token', 12345) == ('Jeffrey', ????????) # TODO not sure what the members data type is

def channel_messages_test():
    # TODO not sure what the messages data type is

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


def channels_list_test ():
    # TODO yo wtf are these fucking data types

def channels_listall_test():
    # TODO yo wtf are these fucking data types

def channels_create_test()
    assert channels_create('valid token', 'Jeffrey', True) == 12345
    with pytest.raises(Exception): # Following should raise exceptions
        assert channels_create('valid token', 'This is a string that is much longer than the max length', True)
<<<<<<< HEAD
=======

def user_profile_setname_test():
    pass

def user_profile_setemail_test():
    pass

def user_profile_sethandle_test():
    pass

def user_profiles_uploadphoto_test():
    pass

def standup_start_test():
    pass

def standup_send_test():
    pass

def search_test():
    pass

def admin_userpermission_change_test():
    pass
>>>>>>> f69836370c157b83114f2b20b6adf9c1a34b700f
