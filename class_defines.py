accounts = [] # list of ALL users

class user():
    def __init__(self, email, password, first, last):
        self.email = email
        self.password = password
        self.name_first = first
        self.name_last = last

channels = [] # list of channels

class channel():
    def __init__(self, owners, admins, members):
        self.owners = []
        self.admins = []
        self.members = []
        # later: self.messages = [], self.pinned_messages = []


# a list of messages
Messages = []

class Mesg:
    def __init__(self, sender, create_time, message):
        self.message = message
        self.sender = sender
        self.create_time = create_time
        self.reaction = None
        self.pin = False

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

