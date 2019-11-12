'''
defination of different slackr classes
'''
perm_owner = 1
perm_admin = 2
perm_member = 3

class User():
    def __init__(self, email, password, first, last, handle, token, user_id):
        self.email = email
        self.password = password
        self.name_first = first
        self.name_last = last
        self.handle = handle
        self.u_id = user_id
        self.token = token      # login token, MAKE SURE it is a string type
        self.prof_pic = ''      # URL to pic
        self.in_channel = []    # list of channels the user is in, stored as channel_id
        self.reset_code = ''
        self.perm_id = perm_member # For slackr permissions

class Channel():
    def __init__(self, name, is_public, channel_id, standup_time):
        # TODO may need to change permission structure
        self.owners = []                    # list of users
        self.members = []                   # list of users
        self.name = name                    # name of channel
        self.messages = []                  # list of messages
        self.is_public = is_public          # public status
        self.channel_id = channel_id        # unique channel id
        self.is_standup = False             # standup flag
        self.standup_time = standup_time    # standup_time start - any variable can be passed in as long as is_standup is False
        self.standup_messages = []          # list of standup messages - cleared after every standup

class Mesg:
    def __init__(self, sender, create_time, message, message_id, channel_id, is_later):
        self.message = message          # string
        self.message_id = message_id    # string of a unique id
        self.sender = sender            # type sender
        self.create_time = create_time  # date_time (depends on is_later)
        self.in_channel = channel_id    # channel id of which the message is blong to
        self.reaction = None            # active reaction
        self.reacted_user = []          # list of user ids that has reacted to this message
        self.is_pinned = False          # pin flag
        self.is_later = is_later        # when to send message
        self.is_unread = True           # read or not

class Reacts():
    def __init__(self, reacter, react_id):
        self.reacter = reacter          # type user
        self.react_id = react_id        # react id of the reaction (for iteration 2 this is 1)

# class Threads(threading.Thread):
#     def __init__(self, time):
#         self.time = time                # either standup_end time or message_send time

data = {
    'accounts': [], #User('chiefjief5@gmail.com', '123456', 'Jeffrey', 'Oh', 'JeffreyOh', '1234', 0), User('kennyhan9831@gmail.com', '1234567', 'Jun', 'Han', 'JunHan', '12345', 1)
    'channels': [Channel('Mychannel', True, 787, False)],
    'account_count': 0,
    'channel_count': 0,
    'message_count': 0,
}
