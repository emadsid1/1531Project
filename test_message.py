'''
Tests for message functions
'''
import pytest
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from channel_functions import channel_create, channel_invite, channel_join, channel_leave, channel_add_owner, channel_remove_owner, channel_details, channel_list, channel_listall, channel_messages
from message import send_later, msg_send, msg_remove, msg_edit, msg_react, msg_unreact, msg_pin, msg_unpin
from profile import user_profile, user_profile_setname, user_profile_email, user_profile_sethandle, user_profile_uploadphoto, users_all, standup_start, standup_active, standup_send, search, admin_userpermission_change
from helper_functions import check_email, user_from_token, user_from_uid, max_20_characters, channel_index, find_channel, find_msg, check_owner, check_admin, check_member, check_in_channel
from Error import AccessError
from datetime import datetime, timedelta
from class_defines import User, Channel, Mesg, Reacts, data
    
def message_sendlater_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing

    # testing end

def message_send_test():
    # setup
    data['accounts'].append(User('email', 'password', 'first', 'last', 'handle', 'token', 12345))
    data['channels'].append(Channel('kenny channel', True, 123456, 15))
    # setup end
    # testing
    assert msg_send('token', 'hello', 1)


    # testing end

def message_remove_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end
    
def message_edit_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end

def message_react_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end

def message_unreact_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end

def message_pin_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end

def message_unpin_test():
    # setup
    user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    channel1 = channel('kenny channel', True, 123456, 15)
    data['accounts'].append(user1)
    data['channels'].append(channel1)
    data['channels'][0].owners.append(user1.u_id)
    data['channels'][0].admins.append(user1.u_id)
    data['channels'][0].members.append(user1.u_id)
    data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # setup end
    # testing
    
    # testing end

