from flask import request    


class ManychatRequest():
    
    request = None
    user_id = None
    full_name = None
    username = None
    telegram_id = None
    tag = None
    id = None
    
    def __init__(self, request):
        self.request = request.get_json()
        self.user_id = self.request['id']
        self.username = self.request['custom_fields']['запит_telegram_username']
        self.telegram_id = self.request['custom_fields']['запит_telegram_id']
        self.full_name = self.request['name']
        self.tag = self.request['custom_fields']['запит_запит']
        self.id = self.request['custom_fields']['request_id']
        print('ManychatRequest', self.request)

    def get_user(self):
        from app.users.models import User
        user = User.get_user_from_manychat(self.user_id)
        if not user:
            user = User.add_user(self.full_name, self.username, self.telegram_id, self.user_id)
        return user
    
    def get_request_tag(self):
        from app.tags.models import Tag
        return Tag.get_by_name(self.tag)
    

    def get_specialist(self):
        from app.specialists.models import Specialist
        return Specialist.find_by_tag(self.get_request_tag())
    


class Response:
    version = 'v2'

    def __init__(self, content):
        self.content = content


    def to_json(self):
        return {
            'version': self.version,
            'content': self.content
        }
    

class ResponseContent:
    def __init__(self, msg_type, messages=None):
        self.type = msg_type
        self.messages = [] if messages is None else messages


    def to_json(self):
        return {
            'type': self.type,
            'messages': [message.to_json() for message in self.messages]
        }




class TextMessage:
    def __init__(self, text, buttons=None):
        self.type = 'text'
        self.text = text
        self.buttons = [] if buttons is None else list(buttons)


    def to_json(self):
        return {
            'type': self.type,
            'text': self.text,
            'buttons': [button.to_json() for button in self.buttons]
        }



class UrlButton:
    def __init__(self, caption: str, url: str):
        self.type = 'url'
        self.caption = caption
        self.url = url


    def to_json(self):
        return {
            'type': self.type,
            'caption': self.caption,
            'url': self.url
        }
