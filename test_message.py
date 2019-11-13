'''
Tests for message functions
'''
import pytest
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from channel import channels_create, channel_invite, channel_join, channel_leave, channel_add_owner, channel_remove_owner, channel_details, channels_list, channels_listall, channel_messages
from message import send_later, msg_send, msg_remove, msg_edit, msg_react, msg_unreact, msg_pin, msg_unpin
from helper_functions import check_email, user_from_token, user_from_uid, max_20_characters, channel_index, find_channel, find_msg, check_owner, check_admin, check_member, check_in_channel
from exception import ValueError, AccessError
from datetime import datetime
from class_defines import User, Channel, Mesg, Reacts, data
    
# setup
auth_register('kenny@gmail.com', 'password', 'kenny', 'han')
auth_register('ken@gmail.com', 'password', 'k', 'h')
auth_register('han@gmail.com', 'password', 'h', 'k')
auth_login('kenny@gmail.com', 'password')
token1 = data['accounts'][0].token
# user 2 does not belong to any channel
auth_login('ken@gmail.com', 'password')
token2 = data['accounts'][1].token
auth_login('han@gmail.com', 'password')
token3 = data['accounts'][2].token
# user 1 is the owner of channel1
channels_create(token1, 'channel1', True)
chan_id1 = data['channels'][0].channel_id
# user 3 is a member of channel1 but not owner
channel_join(token3, chan_id1)
# a long message
long_msg = 'a' * 1000
invalid_msg = 'a' * 1001
# setup end

def test_successful_msg_send():
    # a normal msg
    msg_send(token1, '1st msg', chan_id1)
    assert data['channels'][0].messages[0].message_id == 1
    # a msg with 1000 characters
    msg_send(token3, long_msg, chan_id1)
    assert data['channels'][0].messages[1].message_id == 2
    assert len(data['channels'][0].messages) == 2

def test_msg_too_long():
    # raise ValueError when the message is too long
    with pytest.raises(ValueError):
        msg_send(token1, invalid_msg, chan_id1)

def test_sender_notjoined():
    # raise AccessError when a user does not belong to the channel and tring to send
    with pytest.raises(AccessError):
        msg_send(token2, 'hello', chan_id1)

def message_sendlater_test():
    pass

def test_successful_remove():
    # normal remove
    msg_send(token1, '3rd msg', chan_id1)
    msg_id1 = data['channels'][0].messages[0].message_id
    msg_id3 = data['channels'][0].messages[2].message_id
    assert len(data['channels'][0].messages) == 3
    assert msg_remove(token1, msg_id1) == {}
    assert len(data['channels'][0].messages) == 2
    assert msg_remove(token1, msg_id3) == {}
    assert len(data['channels'][0].messages) == 1

def test_notowner_remove():
    # when remover is not an owner TODO or an admin
    msg_send(token3, '2nd msg', chan_id1)
    msg_id2 = data['channels'][0].messages[1].message_id
    with pytest.raises(AccessError):
        msg_remove(token3, msg_id2)

def test_remover_notsender():
    # when remover is not the actual sender of the message
    msg_send(token3, '3rd msg', chan_id1)
    msg_id3 = data['channels'][0].messages[2].message_id
    with pytest.raises(AccessError):
        msg_remove(token1, msg_id3)

def test_msgid_notexist():
    # when the message_id no longer exist or does not exist
    with pytest.raises(ValueError):
        msg_remove(token1, 12345)
    
def test_successful_edit():
    msg_send(token1, '4th msg', chan_id1)
    msg_id4 = data['channels'][0].messages[3].message_id
    assert msg_edit(token1, msg_id4, 'new 4th msg(edited)') == {}
    assert len(data['channels'][0].messages) == 4

def test_notowner_editor():
    # when editor is not an owner TODO or an admin
    with pytest.raises(AccessError):
        msg_edit(token3, data['channels'][0].messages[0].message_id, 'new msg')

def test_editor_notsender():
    # when editor is not the actual sender of the message
    with pytest.raises(AccessError):
        msg_edit(token1, data['channels'][0].messages[0].message_id, 'new msg')

def message_react_test():
    pass

def message_unreact_test():
    pass

def message_pin_test():
    pass

def message_unpin_test():
    pass

