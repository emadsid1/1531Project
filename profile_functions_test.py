import pytest
import auth_functions, channel_functions, message_functions, profile_functions, helper_functions
from Error import AccessError
from datetime import datetime, timedelta

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
