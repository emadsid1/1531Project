'''
Tests for message functions
'''
import pytest
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from channel import channels_create, channel_invite, channel_join, channel_leave, channel_add_owner, channel_remove_owner, channel_details, channels_list, channels_listall, channel_messages
from profile import admin_userpermission_change
from message import send_later, msg_send, msg_remove, msg_edit, msg_react, msg_unreact, msg_pin, msg_unpin
from helper_functions import check_email, user_from_token, user_from_uid, max_20_characters, channel_index, find_channel, find_msg, check_channel_member, check_channel_owner, check_slackr_admin, check_slackr_owner, check_in_channel
from exception import ValueError, AccessError
from datetime import datetime, timedelta, timezone
from class_defines import User, Channel, Mesg, Reacts, data, perm_admin, perm_owner, perm_member
    
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
    assert msg_send(token1, '1st msg', chan_id1) == {'message_id': 1}
    assert data['channels'][0].messages[0].message_id == 1
    # a msg with 1000 characters
    assert msg_send(token3, long_msg, chan_id1) == {'message_id': 2}
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
    # when remover is not an owner
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
    # when editor is not an owner
    with pytest.raises(AccessError):
        msg_edit(token3, data['channels'][0].messages[0].message_id, 'new msg')

def test_editor_notsender():
    # when editor is not the actual sender of the message
    with pytest.raises(AccessError):
        msg_edit(token1, data['channels'][0].messages[0].message_id, 'new msg')

def test_sendlater_timeinpast():
    # when the time trying to send is in the past
    old_stamp = (datetime.now() - timedelta(days=1)).replace(tzinfo=timezone.utc).timestamp()
    with pytest.raises(ValueError):
        send_later(token1, 'later message', chan_id1, old_stamp)

def test_successful_react():
    # successful thumb up
    user1 = user_from_token(token1)
    msg_id4 = data['channels'][0].messages[3].message_id
    assert msg_react(token1, msg_id4, 1) == {}
    assert data['channels'][0].messages[3].reactions[0].react_id == 1
    assert data['channels'][0].messages[3].reactions[0].reacter == user_from_token(token1).u_id
    assert user1.reacted_msgs[0] == msg_id4

def test_reacted():
    # when the message is already reacted
    msg_id4 = data['channels'][0].messages[3].message_id
    with pytest.raises(ValueError):
        msg_react(token1, msg_id4, 1)

def test_reactid_notvalid():
    # when not passing in 1 as react id
    msg_id3 = data['channels'][0].messages[2].message_id
    with pytest.raises(ValueError):
        msg_react(token1, msg_id3, 2)

def test_react_msgid_notvalid():
    # when the message_id is not valid
    with pytest.raises(ValueError):
        msg_react(token1, 6666, 1)

def test_unreactid_notvalid():
    # when not passing in 1 as (un)react id
    msg_id4 = data['channels'][0].messages[3].message_id
    with pytest.raises(ValueError):
        msg_unreact(token1, msg_id4, 2)

def test_unreact_msgid_notvalid():
    # when the unreact message_id is not valid
    with pytest.raises(ValueError):
        msg_unreact(token1, 6666, 1)

def test_successful_unreact():
    # successful unreact a message that is reacted before
    user1 = user_from_token(token1)
    msg_id4 = data['channels'][0].messages[3].message_id
    assert msg_unreact(token1, msg_id4, 1) == {}
    assert len(data['channels'][0].messages[3].reactions) == 0
    assert len(user1.reacted_msgs) == 0

def test_unreacted():
    # when the message is already unreacted
    msg_id4 = data['channels'][0].messages[3].message_id
    with pytest.raises(ValueError):
        msg_unreact(token1, msg_id4, 1)

def test_successful_pin():                  # TODO check this at the end
    # user1 = user_from_token(token1)
    # user3 = user_from_token(token3)
    # print(user1.u_id)
    print(data['accounts'][0].perm_id)
    # print(user3.u_id)
    # print(user3.perm_id)
    msg_id1 = data['channels'][0].messages[0].message_id
    # admin_userpermission_change(token1, user3.u_id, perm_admin)
    # data['accounts'][0].perm_id == 2
    assert msg_pin(token1, msg_id1) == {}

def test_already_pinned():
    # if the message is already pinned
    msg_id1 = data['channels'][0].messages[0].message_id
    with pytest.raises(ValueError):
        msg_pin(token1, msg_id1)

def test_notmember_pin():
    # if the pinner is a member of the channel
    msg_id1 = data['channels'][0].messages[0].message_id
    with pytest.raises(AccessError):
        msg_pin(token2, msg_id1)

def test_pin_msgid_notvalid():
    # if the message id is not valid
    with pytest.raises(ValueError):
        msg_pin(token1, 6666)

def test_successful_unpin():                  # TODO check this at the end
    msg_id1 = data['channels'][0].messages[0].message_id
    # admin_userpermission_change(token1, user3.u_id, perm_admin)
    # data['accounts'][0].perm_id == 2
    assert msg_unpin(token1, msg_id1) == {}

def test_already_unpinned():
    # if the message is already unpinned
    msg_id1 = data['channels'][0].messages[0].message_id
    with pytest.raises(ValueError):
        msg_unpin(token1, msg_id1)

def test_notmember_unpin():
    # if the unpinner is a member of the channel
    msg_id1 = data['channels'][0].messages[0].message_id
    with pytest.raises(AccessError):
        msg_unpin(token2, msg_id1)

def test_unpin_msgid_notvalid():
    # if the message id is not valid
    with pytest.raises(ValueError):
        msg_unpin(token1, 6666)
