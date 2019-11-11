'''
Tests for message functions
'''
import pytest
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from channel_functions import channels_create, channel_invite, channel_join, channel_leave, channel_add_owner, channel_remove_owner, channel_details, channels_list, channels_listall, channel_messages
from message import send_later, msg_send, msg_remove, msg_edit, msg_react, msg_unreact, msg_pin, msg_unpin
# from profile import user_profile, user_profile_setname, user_profile_email, user_profile_sethandle, user_profile_uploadphoto, users_all, standup_start, standup_active, standup_send, search, admin_userpermission_change
from helper_functions import check_email, user_from_token, user_from_uid, max_20_characters, channel_index, find_channel, find_msg, check_owner, check_admin, check_member, check_in_channel
from exception import ValueError, AccessError
from datetime import datetime
from class_defines import User, Channel, Mesg, Reacts, data
    
# setup
auth_register('kenny@gmail.com', 'password', 'kenny', 'han')
auth_register('han@gmail.com', 'password', 'k', 'h')
auth_login('kenny@gmail.com', 'password')
token1 = data['accounts'][0].token
auth_login('han@gmail.com', 'password')
token2 = data['accounts'][1].token
# user 1 is the owner member of channel1 where user 2 is not
channels_create(token1, 'channel1', True)
chan_id1 = data['channels'][0].channel_id
# a long message
long_msg = 'a' * 1000
invalid_msg = 'a' * 1001
# setup end

def test_successful_msg_send():
    # a normal msg
    msg_send(token1, 'hello', chan_id1)
    assert data['channels'][0].messages[0].message_id == 1
    # a msg with 1000 characters
    msg_send(token1, long_msg, chan_id1)
    assert data['channels'][0].messages[1].message_id == 2

def test_msg_too_long():
    # raise ValueError when the message is too long
    with pytest.raises(ValueError):
        msg_send(token1, invalid_msg, chan_id1)

def test_msgsend_accesserror():
    # raise AccessError when a user does not belong to the channel and tring to send
    with pytest.raises(AccessError):
        msg_send(token2, 'hello', chan_id1)

def message_sendlater_test():
    pass

def message_remove_test():
    pass
    
def message_edit_test():
    pass

def message_react_test():
    pass

def message_unreact_test():
    pass

def message_pin_test():
    pass

def message_unpin_test():
    pass

