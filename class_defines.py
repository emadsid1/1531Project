data = {
    'accounts': [],
    'channels': []
}

class user():
    def __init__(self, email, password, first, last):
        self.email = email
        self.password = password
        self.name_first = first
        self.name_last = last   
        self.handle = ''
        self.user_id = ''
        self.prof_pic = ''  # URL to pic
        self.token = '' # login token
        self.in_channel = []    # list of channels the user is in

class channel():
    def __init__(self, owners, admins, members, name, is_public): 
        self.owners = []    # list of users
        self.admins = []    # list of users admins cant change owner permissions
        self.members = []   # list of users
        self.name = ''  # name of channel
        self.messages = []  # list of messages
        self.is_public = is_public # public status

class mesg:
    def __init__(self, sender, create_time, message, is_later):
        self.message = message  # string
        self.sender = sender    # type user
        self.create_time = create_time  # date_time (depends on is_later)
        self.reaction = []    # facebooks reacts similar list of
        self.pin = False    # pin flag
        self.is_later = is_later    # when to send message

    def get_mesg():
        return self.message

    def get_sender():
        return self.sender

    def get_mesg_time():
        return self.create_time

    def set_reaction(self, reaction):
        self.reaction = reaction

    def remove_reaction(self):
        self.reaction = None

    def pin_self(self):
        self.pin = True

    def unpin_self(self):
        self.pin = False

class reacts():
    def __init__(self, reacter, react_type):
        self.reacter = reacter    # type user
        self.react = react_type # type of reaction (string)



