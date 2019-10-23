accounts = [] # list of classes

class user():
    def __init__(self, email, password, first, last):
        self.email = email
        self.password = password
        self.name_first = first
        self.name_last = last

channels = []

class channel():
    def __init__(self, owners, admins, members):
        self.owners = []
        self.admins = []
        self.members = []
        # later: self.messages = [], self.pinned_messages = []