'''all helper functions'''
import re
from exception import ValueError, AccessError
from class_defines import data, User, Channel, perm_admin, perm_owner, perm_member

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
        if acc.token == token:
            return acc
    raise AccessError(description = 'token does not exist for any user')

def user_from_uid(u_id):
    global data
    for acc in data['accounts']:
        if acc.u_id == u_id:
            return acc
    raise AccessError(description = 'u_id does not exist for any user')

def max_20_characters(name):
    if len(name) <= 20:
        return True
    else:
        return False

def channel_index(channel_id):
    global data
    for i, chan in enumerate(data['channels']):
        if int(chan.channel_id) == int(channel_id):
            return i
    raise ValueError(description = 'channel does not exist')

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
        raise ValueError(description='Channel does not exit, please join or create a channel first!')

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
        raise ValueError(description='Message does not exists!')

# check whether the message already contain a react with the react_id, also find the correct reaction base on the react id
def reaction_exist(reactions, r_id):
    for react in reactions:
        if react.react_id == r_id:
            return react
    return False

# check if a user is an owner of a given channel
def check_channel_owner(channel, u_id):
    global data
    for user_id in channel.owners:
        if user_id == u_id:
            return True
    return False

# check if a user is an member of a given channel
def check_channel_member(channel, u_id):
    for user_id in channel.members:
        if user_id == u_id:
            return True
    return False

# check if a user is an owner of the slackr app
def check_slackr_owner(user):
    if user.perm_id == perm_owner:
        return True
    return False

# check if a user is an admin of the slackr app
def check_slackr_admin(user):
    if user.perm_id == perm_admin or user.perm_id == perm_owner:
        return True
    return False

# Helper from Ben's profile and standup
def check_in_channel(u_id, channel):
    # in_channel = False
    # for user_id in channel.owners: # search owners list
    #     if user_id == u_id:
    #         in_channel = True
    # # if in_channel == False:
    # #     for acc in data["channels"][channel_index].admins: # search admins list
    # #         if token == acc.token:
    # #             in_channel = True
    # if in_channel == False:
    #     for acc in channel.members: # search members list
    #         if token == acc.token:
    #             in_channel = True
    in_channel = check_channel_owner(channel, u_id)
    if in_channel == False:
        in_channel = check_channel_member(channel, u_id)
    if in_channel == False: # if the user is not in the channel, raise an error
        raise AccessError(description="You are currently not in this channel.")

def get_reacts(user, message):
    # This is only used if we can't assume that there is only one react_id
    # react_dict = {}
    # react_id_list = []
    # user_id_list = []
    # #is_this_user_reacted = []
    # for r in message.reactions: # get a list of all different react_ids
    #     if not react_id_list:
    #         react_id_list.append(r.react_id)
    #     elif r.react_id not in react_id_list:
    #         react_id_list.append(r.react_id)
    #
    # for i in range(sizeof(react_id_list)):  # create list of lists
    #     user_id_list.append([])
    #
    # j = 0
    # for reacc in react_id_list: # create a list of a list of u_ids
    #     for type in message.reactions:
    #         if reacc == type.react_id:
    #             user_id_list[j].append(type.reacter.u_id)
    #     j += 1

    reacc = False
    if user.u_id in message.reacted_user:
        reacc = True
    return [{
        "react_id": 1,          # assume only one type of react_id
        "u_ids": message.reacted_user,
        "is_this_user_reacted": reacc
    }]

# End of helper functions
