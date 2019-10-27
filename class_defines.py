data = {
    'accounts': [],
    'channels': []
}

account_count = 0

class user():
    def __init__(self, email, password, first, last, handle, token, user_id):
        self.email = email
        self.password = password
        self.name_first = first
        self.name_last = last
        self.handle = handle
        self.u_id = user_id
        self.token = token # login token
        self.prof_pic = ''  # URL to pic
        self.in_channel = []    # list of channels the user is in
        self.reset_code = ''

class channel():
    def __init__(self, name, is_public, channel_id, standup_time):
        self.owners = []                    # list of users
        self.admins = []                    # list of users admins cant change owner permissions
        self.members = []                   # list of users
        self.name = name                    # name of channel
        self.messages = []                  # list of messages
        self.is_public = is_public          # public status
        self.channel_id = channel_id
        self.is_standup = False             # standup flag
        self.standup_time = standup_time    # standup_time start - any variable can be passed in as long as is_standup is False
        self.standup_messages = []          # list of standup messages - cleared after every standup

    def get_standup_time():
        return self.standup_time

class mesg:
    def __init__(self, sender, create_time, message, message_id, channel_id, is_later):
        self.message = message          # string
        self.message_id = message_id    # string of a unique id
        self.sender = sender            # type user
        self.create_time = create_time  # date_time (depends on is_later)
        self.in_channel = channel_id    # channel id of which the message is blong to
        self.reaction = None            # active reaction
        self.reacted_user = []          # list of user ids that has reacted to this message
        self.is_pinned = False          # pin flag
        self.is_later = is_later        # when to send message
        self.is_unread = True           # read or not

class reacts():
    def __init__(self, reacter, react_type, react_id):
        self.reacter = reacter          # type user
        self.react_type = react_type    # reaction types
        self.react_id = react_id        # react id of the reaction (for iteration 2 this is 1)
