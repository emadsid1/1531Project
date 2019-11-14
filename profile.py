from json import dumps
from class_defines import User, Mesg, Channel, data
from datetime import datetime, timedelta, timezone
from exception import ValueError, AccessError
from helper_functions import find_channel, find_msg, check_admin, check_owner, check_member, user_from_token, user_from_uid
from PIL import image
import urllib.request


# nom = User("naomizhen@gmail.com", "password", "naomi", "zhen", "nomHandle", "12345", 1)
# ben = User("benkah@gmail.com", "password", "ben", "kah", "benHandle", "1234", 2)
# chan1 = Channel("chatime", True, 1, 5)
#
# data = {
#     "accounts": [nom, ben],
#     "channels": [chan1]
# }

# TODO: fix user_profile to work with u_id
def user_profile(token, user_id):
    global data
    # print(user_id)
    user_uid = user_from_uid(user_id) # raises AccessError if u_id invalid
    user_token = user_from_token(token) # raises AccessError if invalid token
    if user_uid != user_token:
        raise ValueError(description = "Token does not match u_id!")
    return {
        "email": user_token.email,
        "name_first": user_token.name_first,
        "name_last": user_token.name_last,
        "handle_str": user_token.handle,
        "profile_img_url": user_token.prof_pic,
        # "token": token,
        # "u_id": user_id
    }

def user_profile_setname(token, name_first, name_last):
    global data
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise ValueError(description = "Name needs to be between 1 and 50 characters long.")
    user = user_from_token(token) # raises AccessError if invalid token
    user.name_first = name_first
    user.name_last = name_last
    # no return statement

def user_profile_email(token, email):
    global data
    check_email(email)
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if email == acc.email:
            raise ValueError(description = "Email already being used!") # email already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].email = email
    else:
        raise AccessError(description = "token does not exist for any user") # token is invalid
    # no return statement

def user_profile_sethandle(token, handle):
    global data
    if len(handle) < 3 or len(handle) > 20:
        raise ValueError(description = "Handle needs to be between 3 and 20 characters.") # handle has incorrect number of chars
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if handle == acc.handle:
            raise ValueError(description = "Handle is already in use.") # handle already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].handle = handle
    else:
        raise AccessError(description = "token does not exist for any user") #token is invalid
    # no return statement

# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    global data
    # how to get image size?
    # TODO: use week 8 slides from lecture
    # imgDown.py
    # crop.py
    # convert the url into something unique (perhaps u_id)
    # static.py
    # [request.host]/static/filename.png
    user = user_from_token(token)
    urrllib.request.urlretrieve(img_url, user.prof_pic)
    imageObject = Image.open(user.prof_pic)
    cropped = imageObject.crop(x_start, y_start, x_end, y_end)
    cropped.save(user.prof_pic)
    directory = request.host()
    return send_from_directory(directory, user.prof_pic)
    # no return statement

def users_all(token):
    global data
    user_list = []
    valid = False
    for acc in data["accounts"]:
        user_list.append({
            "u_id": acc.u_id,
            "email": acc.email,
            "name_first": acc.name_first,
            "name_last": acc.name_last,
            "handle_str": acc.handle,
            "profile_img_url": acc.prof_pic
        })
        if token == acc.token:
            valid = True
    if valid == False:
        raise AccessError(description = "token does not exist for any user") # token is invalid
    return {
        "users": user_list
    }

def standup_start(token, channel, length):
    global data
    chan = find_channel(channel) # raises ValueError if channel does not exist
    if chan.is_standup == True:
        raise AccessError(description = "Standup is already in progress!") # standup is already in progress
    if length <= 0:
        raise ValueError(description = "The standup length needs to be a positive number!") # standup length needs to be greater than 0
    check_in_channel(token, chan) # raises AccessError if user is not in channel

    # starts standup
    chan.is_standup = True
    finish = datetime.now() + timedelta(seconds=length)
    chan.standup_time = finish
    standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()
    t = Timer(length, standup_active, (token, channel))
    t.start()

    return {
        "time_finish": standup_finish
    }

def standup_active(token, channel):
    global data
    chan = find_channel(channel) # raises AccessError if channel does not exist
    #check_in_channel(token, ch_num) # raises AccessError if user is not in channel
    if chan.is_standup == False:
        finish = None
    else:
        if chan.standup_time < datetime.now():
            chan.is_standup = False
            standup_end(token, ch_num) # TODO: write this function
        else:
            finish = chan.standup_time
    return {
        "is_active": chan.is_standup,
        "time_finish": finish
    }

def standup_send(token, channel, message):
    global data
    chan = find_channel(channel) # raises AccessError if channel does not exist
    if chan.is_standup == False:
        raise ValueError(description = "There is no standup currently happening.") # standup is not happening atm
    if len(message) > 1000:
        raise ValueError(description = "Your message is too long.") # message too long
    check_in_channel(token, chan) # raises AccessError if user is not in channel

    # TODO: how to check if standup has finished?
    msg_send(token, message, channel)
    user = user_from_token(token)
    chan.standup_messages.append([user.handle, message])
    # no return statement

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
    return {
        "messages": messages
    }

def admin_userpermission_change(token, u_id, p_id):
    global data
    if not(perm_owner < p_id or p_id < perm_member):
        raise ValueError(description = 'permission_id does not refer to a value permission') # invalid perm_id
    for acc in data['accounts']:
        if acc.token == token:
            if not(acc.perm_id >= p_id):    # does not have permission to change p_id
                raise AccessError(description = 'The authorised user is not an admin or owner')
    for acc in data['accounts']:
        if acc.user_id == u_id:
            acc.perm_id = p_id
            if p_id == perm_member:
                for chan in data['channels']:
                    if u_id in chan.owners:
                        if len(channel.owners) != 1:
                            chan.owners.remove(u_id)
                    if not(u_id in chan.members):
                        chan.members.append(u_id)
            else:
                for chan in data['channels']:
                    if u_id in chan.members:
                        chan.members.remove(u_id)
                    if not(u_id in chan.owners):
                        chan.owners.append(u_id)
            return 0 # TODO: fix this
    raise ValueError(description = 'u_id does not refer to a valid user')
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
    for msg in current_channel.standup_messages:
        msg_user = " ".join(msg)
        message_list.append(msg_user)
    stdup_summary = "\n".join(message_list)
    current_channel.messages.append(Mesg(sender, send_time, stdup_summary, msg_id, channel, False))
