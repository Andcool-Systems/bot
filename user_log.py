class User():
    def __init__(self, username):
        self.username = username
        self.deleted_messages = []
        
    def add_msg(self, msg):
        self.deleted_messages.append(msg)

class Chat():
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.users = []

    def add_user(self, user):
        self.users.append(user)