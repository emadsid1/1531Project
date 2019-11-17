'''profile functions'''
from flask import send_from_directory
from threading import Timer
from class_defines import User, Mesg, Channel, data, perm_member, perm_admin, perm_owner
from datetime import datetime, timedelta, timezone
from exception import ValueError, AccessError
from helper_functions import check_email, find_channel, find_msg, user_from_token, user_from_uid, check_in_channel, get_reacts
from message import msg_send
from PIL import Image
from time import time
import imghdr
import urllib.request


# nom = User("naomizhen@gmail.com", "password", "naomi", "zhen", "nomHandle", "12345", 1)
# ben = User("benkah@gmail.com", "password", "ben", "kah", "benHandle", "1234", 2)
# chan1 = Channel("chatime", True, 1, 5)
#
# data = {
#     "accounts": [nom, ben],
#     "channels": [chan1]
# }

def user_profile(token, user_id):
    global data
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
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise ValueError(description = "Name needs to be between 1 and 50 characters long.")
    user = user_from_token(token) # raises AccessError if invalid token
    user.name_first = name_first
    user.name_last = name_last
    return {}

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
    return {}

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
    return {}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, host):
    global data
    user = user_from_token(token)
    img_loc = f'./static/{user.handle}.jpg' # Location to store file
    urllib.request.urlretrieve(img_url, img_loc)
    if imghdr.what(img_loc) != 'jpeg':
       raise ValueError(description = 'the file is not of type jpg')
    prof_image = Image.open(img_loc)
    (width, height) = prof_image.size
    if not(0 <= x_start and x_start <= width and 0 <= y_start and y_start <= height) or not(x_start < x_end and y_start < y_end):
            raise ValueError(description = 'the dimensions are not within the size of the image')
    box = (x_start, y_start, x_end, y_end)
    cropped = prof_image.crop(box)
    cropped.save(img_loc)
    user.prof_pic = f'{host}static/{user.handle}.jpg'
    return {}

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
        raise ValueError(description = "Standup is already in progress!") # standup is already in progress
    if length <= 0:
        raise ValueError(description = "The standup length needs to be a positive number!") # standup length needs to be greater than 0
    user = user_from_token(token)
    check_in_channel(user.u_id, chan) # raises AccessError if user is not in channel

    # starts standup
    chan.is_standup = True
    # finish = datetime.now() + timedelta(seconds=length)
    # standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()
    standup_finish = time() + float(length)
    chan.standup_time = standup_finish
    # chan.standup_time = finish.replace(tzinfo=timezone.utc).timestamp()
    t = Timer(length, standup_active, (token, channel))
    t.start()

    return {
        "time_finish": standup_finish
    }

def standup_active(token, channel):
    global data
    chan = find_channel(channel) # raises AccessError if channel does not exist
    user = user_from_token(token)
    check_in_channel(user.u_id, chan) # raises AccessError if user is not in channel
    finish = None
    if chan.is_standup == True:
        # if chan.standup_time < datetime.now().replace(tzinfo=timezone.utc).timestamp():
        if chan.standup_time < time():
            chan.is_standup = False
            standup_end(token, chan.channel_id)
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
    user = user_from_token(token)
    check_in_channel(user.u_id, chan) # raises AccessError if user is not in channel

    msg_send(token, message, channel)
    user = user_from_token(token)
    chan.standup_messages.append([user.handle, message])
    return {}

def search(token, query_str):
    global data
    user = user_from_token(token)
    messages = []
    for ch in user.in_channel: # in_channel is a list of channel_ids
        chan = find_channel(ch)
        for msg in chan.messages:
            if query_str in msg.message:
                reaction = get_reacts(user, msg)
                messages.append({
                    "message_id": msg.message_id,
                    "u_id": msg.sender,
                    "message": msg.message,
                    "time_created": msg.create_time,
                    "reacts": reaction,
                    "is_pinned": msg.is_pinned
                })
    return {
        "messages": messages
    }

def admin_userpermission_change(token, u_id, p_id):
    global data
    if not(perm_owner <= p_id and p_id <= perm_member):
        raise ValueError(description = 'permission_id does not refer to a value permission') # invalid perm_id
    c_user = user_from_token(token)
    if c_user.perm_id > p_id:
        raise AccessError(description = 'The authorised user is not an admin or owner')
    p_user = user_from_uid(u_id)
    if p_user.perm_id < c_user.perm_id:
        raise AccessError(description = 'The authorised user is not an admin or owner')
    p_user.perm_id = p_id
    return {}

# not included in the function list, but useful to have
# sends the summary of the standup messages
def standup_end(token, channel):
    global data
    current_channel = find_channel(channel)
    message_list = []
    for msg in current_channel.standup_messages:
        msg_user = ": ".join(msg)
        message_list.append(msg_user)
    stdup_summary = "\n".join(message_list)
    msg_send(token, stdup_summary, current_channel.channel_id)
