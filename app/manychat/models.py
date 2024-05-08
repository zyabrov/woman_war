from flask import request    
import requests



class ManychatRequest():
    request = None
    user_id = None
    full_name = None
    username = None
    telegram_id = None
    tag_name = None
    id = None
    birthdate = None
    where_is = None
    where_is_city = None
    worked_with_psychologist_before = None
    help_type = None
    how_known = None
    phone = None
    
    
    def __init__(self, request):
        self.request = request.get_json()
        self.user_id = self.request['id']
        self.username = self.request['custom_fields']['запит_telegram_username']
        self.telegram_id = self.request['custom_fields']['запит_telegram_id']
        self.full_name = self.request['custom_fields']["опитування_ім'я"]
        self.tag_name = self.request['custom_fields']['запит_запит']
        self.id = self.request['custom_fields']['request_id']
        self.birthdate = self.request['custom_fields']['опитування_дата_народження']
        self.where_is = self.request['custom_fields']['Опитування_де_знаходиться']
        self.where_is_city = self.request['custom_fields']['опитування_місто']
        self.worked_with_psychologist_before = self.request['custom_fields']['запит_досвід_з_психологом']
        self.help_type = self.request['custom_fields']['опитування_яку_допомогу']
        self.how_known = self.request['custom_fields']['запит_як_дізналися']
        self.phone = self.request['phone']
        print('ManychatRequest', self.request)
    
    def get_request_tag(self):
        from app.tags.models import Tag
        return Tag.get_by_name(self.tag_name)
    

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
            'messages': self.messages
        }

class ImageMessage:
    def __init__(self, image_url):
        self.type = 'image'
        self.url = image_url

    
    def to_json(self):
        return {
            'type': self.type,
            'url': self.url
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





class SendContent():
    url = 'https://api.manychat.com/fb/sending/sendContent'
    API_TOKEN = '539030:b5bb217ba67cc15f9059df99e175a204'
    headers = {
        'Authorization': 'Bearer ' + API_TOKEN,
        'Content-Type': 'application/json'
    }

    def __init__(self, subscriber_id, data: ResponseContent, message_tag, otn_topic_name):
        self.subscriber_id = subscriber_id
        self.data = data
        self.message_tag = message_tag
        self.otn_topic_name = otn_topic_name
        
    
    def to_json(self):
        return {
            'subscriber_id': self.subscriber_id,
            'data': self.data,
            'message_tag': self.message_tag,
            'otn_topic_name': self.otn_topic_name
        }
    
    def post(self):
        r = requests.post(self.url, json=self.to_json(), headers=self.headers)
        r.raise_for_status()
