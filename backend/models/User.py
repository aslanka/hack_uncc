class User:
    def __init__(self, name, email, password, friends_list, pending_friend_request):
        self.name = name
        self.email = email
        self.friends_list = friends_list
        self.pending_friend_request = pending_friend_request
  

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'friends_list': self.friends_list,
            'pending_friend_request': pending_friend_request
        
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            friends_List = data['freinds_list'],
            pending_friend_request = data['pending_friend_request']
        )
