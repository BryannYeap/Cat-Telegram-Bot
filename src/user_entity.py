import json

class User_Entity:
    def __init__(self, user_id, username, name, breed, no_of_photos, is_gif):
        self.user_id = str(user_id)
        self.username = username
        self.name = name
        self.breed = breed
        self.no_of_photos = no_of_photos
        self.is_gif = is_gif

    def __repr__(self):
        return json.dumps(self.__dict__)