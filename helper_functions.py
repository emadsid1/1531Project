import re
from exception import ValueError, AccessError
from class_defines import data, User, Channel

# Helper functions
# Helper from jeff's auth
def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not(re.search(regex,email))):    # if not valid email
        raise ValueError(description = 'not a valid email')
    return

# Helpers from Emad's channel
# channel invite vs join, invite needed to join a private channel. passive v active.
# given a token, returns acc with that token
def user_from_token(token):
    global data
    for acc in data['accounts']:
        #print(acc)
        if acc.token == token:
            return acc
    raise AccessError('token does not exist for any user')

# given u_id, returns acc with that u_id
def user_from_uid(u_id):
    global data
    for acc in data['accounts']:
        if acc.u_id == u_id:
            return acc
    raise AccessError('u_id does not exist for any user')

def max_20_characters(name):
    if len(name) <= 20:
        return True
    else:
        return False

def channel_index(channel_id):
    global data
    index = 0
    for i in data['channels']:
        if i.channel_id == channel_id:
            return index
        index = index + 1
    raise ValueError('channel does not exist')

# Helpers from kenny's message
# find the correct channel base on the channel_id
def find_channel(chan_id):
    global data
    channel_found = False
    for chan in data['channels']:
        if chan.channel_id == chan_id:
            channel_found = True
            return chan
    if channel_found == False:
        raise AccessError('Channel does not exit, please join or create a channel first!')

# find the correct message base on the message_id
def find_msg(msg_id):
    global data
    message_found = False
    for chan in data['channels']:
        for msg in chan.messages:
            if msg.message_id == msg_id:
                message_found = True
                return msg
    if message_found == False:
        raise ValueError('Message does not exists!')

# check if a user is an owner of a given channel
def check_owner(channel, u_id):
    global data
    for user_id in channel.owners:
        if user_id == u_id:
            return True
    return False

# check if a user is an admin of a given channel
def check_admin(channel, u_id):
    for user_id in channel.admins:
        if user_id == u_id:
            return True
    return False

# check if a user is an member of a given channel
def check_member(channel, u_id):
    for user_id in channel.members:
        if user_id == u_id:
            return True
    return False

# Helper from Ben's profile and standup
def check_in_channel(token, channel_index):
    in_channel = False
    for acc in data["channels"][channel_index].owners: # search owners list
        if token == acc.token:
            in_channel = True
    if in_channel == False:
        for acc in data["channels"][channel_index].admins: # search admins list
            if token == acc.token:
                in_channel = True
    if in_channel == False:
        for acc in data["channels"][channel_index].members: # search members list
            if token == acc.token:
                in_channel = True
    if in_channel == False: # if the user is not in the channel, raise an error
        raise AccessError("You are currently not in this channel.") # TODO: need to write this function
# End of helper functions