from json import dumps
from class_defines import User, Mesg, data
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from Error import AccessError
from message import msg_send
from helper_functions import find_channel, find_msg, check_admin, check_owner, check_member, user_from_token, user_from_uid

# nom = User("naomizhen@gmail.com", "password", "naomi", "zhen", "nomHandle", "12345", 1)
# ben = User("benkah@gmail.com", "password", "ben", "kah", "benHandle", "1234", 2)
# chan1 = channel("chatime", True, 1, 5)
#
# data = {
#     "accounts": [nom, ben],
#     "channels": [chan1]
# }

def user_profile(token):
    global data
    valid = False
    user = {}
    for acc in data["accounts"]:
        if token == acc.token: # note: assumes token is valid
            valid = True
            if int(request.args.get("u_id")) == acc.u_id:
                user["email"] = acc.email
                user["name_first"] = acc.name_first
                user["name_last"] = acc.name_last
                user["handle_str"] = acc.handle
            else:
                raise Exception("ValueError") # wrong u_id
    if valid == False:
        raise Exception("AccessError") # invalid token
    return dumps({
    "email": user["email"],
    "name_first": user["name_first"],
    "name_last": user["name_last"],
    "handle_str": user["handle_str"]
    })

def user_profile_setname(token, name_first, name_last):
    global data
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise Exception("ValueError")
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise Exception("ValueError")

    for acc in data["accounts"]:
        if token == acc.token:
            acc.name_first = name_first
            acc.name_last = name_last
        else:
            raise Exception("AccessError") # invalid token
    return dumps({})


def user_profile_email(token, email):
    global data
    check_email(email)
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if email == acc.email:
            raise Exception("ValueError") # email already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].email = email
    else:
        raise Exception("AccessError") # token is invalid
    return dumps({})

def user_profile_sethandle(token, handle):
    global data
    if len(handle) < 3 or len(handle) > 20:
        raise Exception("ValueError") # handle has incorrect number of chars
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if handle == acc.handle:
            raise Exception("ValueError") # handle already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].handle = handle
    else:
        raise Exception("AccessError") #token is invalid
    return dumps({})

# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def user_profile_uploadphoto():
    global data
    request = request.get("img_url")
    if request != 200:
        raise Exception("ValueError")
    url = request.form.get("img_url")
    # how to get image size?
    return dumps({})

def users_all(token):
    global data
    user_list = []
    valid = False
    for acc in data["accounts"]:
        user_list.append(acc)
        if token == acc.token:
            valid = True
    if valid == False:
        raise Exception("AccessError") # token is invalid
    return dumps(user_list)

def standup_start(token, channel, length):
    global data
    ch_num = find_channel(channel) # raises ValueError if channel does not exist
    if data["channels"][ch_num].is_standup == True:
        raise Exception("AccessError") # standup is already in progress
    if length <= 0:
        raise Exception("ValueError") # standup length needs to be greater than 0
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel

    # starts standup
    data["channels"][ch_num].is_standup = True
    finish = datetime.now() + timedelta(seconds=length)
    data["channels"][ch_num].standup_time = finish
    standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()
    t = Timer(length, standup_active, (token, channel))
    t.start()

    return dumps({
        "time_finish": standup_finish
    })

def standup_active(token, channel):
    global data
    ch_num = find_channel(channel) # raises AccessError if channel does not exist
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel
    if data["channels"][ch_num].is_standup == False:
        finish = None
    else:
        if data["channels"][ch_num].standup_time < datetime.now():
            data["channels"][ch_num].is_standup = False
            standup_end(token, ch_num) # TODO: write this function
        else:
            finish = data["channels"][ch_num].standup_time
    return dumps({
        "is_active": data["channels"][ch_num].is_standup,
        "time_finish": finish
    })

def standup_send(token, channel, message):
    global data
    ch_num = find_channel(channel) # raises AccessError if channel does not exist
    if data["channels"][ch_num].is_standup == False:
        raise Exception("ValueError") # standup is not happening atm
    if len(message) > 1000:
        raise Exception("ValueError") # message too long
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel

    # TODO: how to check if standup has finished?
    msg_send(token, message, channel)
    user_index = user_from_token(token)
    user = data["accounts"][user_index].handle
    data["channels"][ch_num].standup_messages.append([user, message])
    return dumps({})

def search(token, query_str):
    global data
    for acc in data["accounts"]:
        if token == acc.token:
            ch_list = acc.in_channel
    messages = []
    for ch in ch_list: # assume in_channel object is list of channel classes
        for msg in ch.messages:
            if query_str in msg.message:
                messages.append({
                    "message_id": msg.message_id,
                    "u_id": msg.sender.user_id,
                    "message": msg.message,
                    "time_created": msg.create_time,
                    "reacts": msg.reaction,
                    "is_pinned": msg.pin
                })

    return dumps({messages})

def admin_userpermission_change(token, u_id, p_id):
    global data
    if not(perm_owner < p_id or p_id < perm_member):
        raise ValueError('permission_id does not refer to a value permission') # invalid perm_id
    for acc in data['accounts']:
        if acc.token == token:
            if not(acc.perm_id >= p_id):    # does not have permission to change p_id
                raise AccessError('The authorised user is not an admin or owner')
    # CHECK how users stored in channels
    for acc in data['accounts']:
        if acc.user_id == u_id:
            acc.perm_id = p_id
            if p_id == perm_member:
                for chan in data['channels']:
                    if u_id in chan.owners:
                        chan.owners.remove(u_id)
                    if not(u_id in chan.members):
                        chan.members.append(u_id)
            else:
                for chan in data['channels']:
                    if u_id in chan.members:
                        chan.members.remove(u_id)
                    if not(u_id in chan.owners):
                        chan.owners.append(u_id)
            return dumps({})
    raise ValueError('u_id does not refer to a valid user')
    # for ch in data["channels"]:
    #     for own in ch.owners:
    #         if token == own.token:
    #             has_permission = True
    #         if user_id == acc.user_id:
    #             valid = True
    #             if perm_id != 1:
    #                 remove(own)
    #                 user = own
    #     for ad in ch.admins:
    #         if token == ad.token:
    #             has_permission = True
    #         if user_id == acc.user_id:
    #             valid = True
    #             if perm_id != 2:
    #                 remove(acc)
    #                 user = acc
    #     for mem in ch.members:
    #         if user_id == acc.user_id:
    #             valid = True
    #             if perm_id != 3:
    #                 remove(mem)
    #                 user = mem
    # if has_permission == False:
    #     raise Exception("AccessError") # members cannot use this function
    # if valid == False:
    #     raise Exception("ValueError") # user does not exist
    # for add in data["channels"]:
    #     if perm_id == 1:
    #         add.owners.append(user)
    #     if perm_id == 2:
    #         add.admins.append(user)
    #     if perm_id == 3:
    #         add.members.append(user)
    # return dumps({})

# not included in the function list, but useful to have
# sends the summary of the standup messages
def standup_end(token, channel):
    global data
    send_time = datetime.now()
    sender = user_from_token(token)
    current_channel = find_channel(channel)
    message_id = int(uuid4())
    message_list = []
    for msg in data["channels"][channel].standup_messages:
        msg_user = " ".join(msg)
        message_list.append(msg_user)
    stdup_summary = "\n".join(message_list)
    current_channel.messages.append(Mesg(sender, send_time, stdup_summary, msg_id, channel, False))
