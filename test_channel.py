'''
tests for channel functions
'''

def test_channels_create():
    with pytest.raises(Exception): # Following should raise exceptions
        channels_create('valid token', 'This is a string that is much longer than the max length', True)

def test_channel_invite():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail@gmail.com", "password123456", "John", "Smith"))
    token = auth_register_dict['token']

    auth_register_dict2 = json.loads(auth_register("emad@gmail.com", "password142256", "Emad", "Siddiqui"))
    token2 = auth_register_dict2['token']

    auth_register_dict3 = json.loads(auth_register("email@gmail.com", "password13456", "Firstname", "Lastname"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = channels_create(token, "tokenchannel", True) # create token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    channel_invite(token, channel_id, uid3)
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token2, channel_id, uid3) #AccessError since token2 is not authorised
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, channel_id, (uid3+8)) #ValueError since u_id does not exist

def test_channel_join():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail1@gmail.com", "password123456", "John1", "Smith1"))
    token = auth_register_dict['token']

    auth_register_dict2 = json.loads(auth_register("emad1@gmail.com", "password142256", "Emad1", "Siddiqui1"))
    token2 = auth_register_dict2['token']

    auth_register_dict3 = json.loads(auth_register("email1@gmail.com", "password13456", "Firstname1", "Lastname1"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = channels_create(token, "tokenchannel1", False) # create PRIVATE token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_join(token2, channel_id) #channel is PRIVATE & token2 is not an admin
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_invite(token, 00000000000, uid3) #ValueError since channel_id does not exist

def test_channel_leave():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail2@gmail.com", "password123456", "John2", "Smith2"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad2@gmail.com", "password142256", "Emad2", "Siddiqui2"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']

    auth_register_dict3 = json.loads(auth_register("email2@gmail.com", "password13456", "Firstname2", "Lastname2"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = channels_create(token, "tokenchannel2", False) # create PRIVATE token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_leave(token, 00000000000) #ValueError since channel_id does not exist

    with pytest.raises(Exception): # Following should raise exceptions
        channel_leave(token2, channel_id) # token2 is not a part of channel_id, AccessError

    channel_invite(token, channel_id, uid2) # add token2 to channel
    # assert that uid2 has been added
    assert json.loads(channel_details(token, channel_id))['members'] == [uid, uid2]

    channel_leave(token2, channel_id) # should work as now token2 is part of channel
    # assert that uid2 has been deleted
    assert json.loads(channel_details(token, channel_id))['members'] == [uid] 

def test_channel_add_owner():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail3@gmail.com", "password123456", "John3", "Smith3"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad3@gmail.com", "password142256", "Emad3", "Siddiqui3"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']

    auth_register_dict3 = json.loads(auth_register("email3@gmail.com", "password13456", "Firstname3", "Lastname3"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = channels_create(token, "tokenchannel3", False) # create PRIVATE token's channel
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_add_owner(token, 00000000000, uid2) #ValueError since channel_id does not exist

    with pytest.raises(Exception): # Following should raise exceptions
        channel_add_owner(token, channel_id, uid) # ValueError, u_id is already an owner
    
    with pytest.raises(Exception): # Following should raise exceptions
        channel_add_owner(token2, channel_id, uid3) # AccessError token2 is not an owner of slackr or channel
    
    channel_add_owner(token, channel_id, uid2) # make token2 an owner
    assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]
    channel_add_owner(token2, channel_id, uid3) # Exception should now not be raised
    assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2, uid3]

def test_channel_remove_owner():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail4@gmail.com", "password123456", "John4", "Smith4"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad4@gmail.com", "password142256", "Emad4", "Siddiqui4"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']

    auth_register_dict3 = json.loads(auth_register("email4@gmail.com", "password13456", "Firstname4", "Lastname4"))
    uid3 = auth_register_dict3['u_id']

    channel_dict = channels_create(token, "tokenchannel4", True)
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_remove_owner(token, 00000000000, uid2) # ValueError since channel_id does not exist

    with pytest.raises(Exception): # Following should raise exceptions
        channel_remove_owner(token2, channel_id, uid3) # AccessError since token2 is not an owner of slackr or channel

    with pytest.raises(Exception): # Following should raise exceptions
        channel_remove_owner(token, channel_id, uid2) # ValueError since uid2 is not an owner
    
    channel_add_owner(token, channel_id, uid2) # make uid2 an owner
    assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]
    channel_remove_owner(token, channel_id, uid2) # Exception should now not be raised
    assert json.loads(channel_details(token, channel_id))['owners'] == [uid]

def test_channel_details():
    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail5@gmail.com", "password123456", "John5", "Smith5"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad5@gmail.com", "password142256", "Emad5", "Siddiqui5"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']

    channel_dict = channels_create(token, "tokenchannel5", True)
    channel_id = channel_dict['channel_id']
    #SETUP END

    with pytest.raises(Exception): # Following should raise exceptions
        channel_details(token, 000000) # ValueError since channel_id does not exist

    with pytest.raises(Exception): # Following should raise exceptions
        channel_details(token2, channel_id) # AccessError since token2 is not in channel
    
    # channel_details has been further tested in the asserts of other test functions, 
    # such as assert json.loads(channel_details(token, channel_id))['owners'] == [uid, uid2]

def test_channels_list():
    # empty data['channels'] & ['accounts'] since it may be populated from other tests
    data['channels'].clear
    data['accounts'].clear

    #SETUP START
    auth_register_dict = json.loads(auth_register("goodemail6@gmail.com", "password123456", "John6", "Smith6"))
    token = auth_register_dict['token']
    uid = auth_register_dict['u_id']

    auth_register_dict2 = json.loads(auth_register("emad6@gmail.com", "password142256", "Emad6", "Siddiqui6"))
    token2 = auth_register_dict2['token']
    uid2 = auth_register_dict2['u_id']
    #SETUP END

    channel_dict = channels_create(token, "tokenchannel6", True) # token1's channel
    channel_id = channel_dict['channel_id']
    
    channel_dict2 = channels_create(token2, "token2channel6", True) # token2's channel
    channel_id2 = channel_dict2['channel_id']

    list_dict = channels_list(token) # should work
    assert channels_list(token)['channels'] == [{'channel_id':channel_id, 'name':"tokenchannel6"}] # displays token1's channel only
    assert channels_list(token2)['channels'] == [{'channel_id':channel_id2, 'name':"token2channel6"}] # displays token2's channel only

def test_channels_listall():
    # empty data['channels'] & ['accounts'] since it may be populated from other tests
    data['channels'].clear
    data['accounts'].clear

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

    #assert json.loads(channels_listall(token))['channels'] == [{'channel_id':channel_id, 'name':"tokenchannel6"}] # displays token1's channel only

    channel_dict2 = channels_create(token2, "token2channel", True) # token1's channel
    channel_id = channel_dict2['channel_id']

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
