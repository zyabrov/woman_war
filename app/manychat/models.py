from flask import request    
import requests



class ManychatRequest():    
    def __init__(self, request):
        self.user_id = request['id']
        self.username = request['custom_fields'].get('telegram_username', None)
        self.telegram_id = request['custom_fields']['telegram_id']
        self.full_name = request['custom_fields']["опитування_ім'я"]
        self.tag_name = request['custom_fields']['запит_запит']
        self.id = request['custom_fields']['request_id']
        self.birthdate = request['custom_fields']['опитування_дата_народження']
        self.where_is = request['custom_fields']['Опитування_де_знаходиться']
        self.where_is_city = request['custom_fields']['опитування_місто']
        self.worked_with_psychologist_before = request['custom_fields']['запит_досвід_з_психологом']
        self.help_type = request['custom_fields']['опитування_яку_допомогу']
        self.how_known = request['custom_fields']['запит_як_дізналися']
        self.phone = request['phone']
        self.group_name = request['custom_fields'].get('запит_група', None)
        self.request_type = request['custom_fields']['тип_запиту']
        self.manychat_username = request['name']
        self.message_id = request['custom_fields'].get('request_message_id')
        self.user_request_id = request['custom_fields'].get('підтвердження_запиту_id', None)
        self.manychat_img = request['profile_pic']
        self.user_age = request['custom_fields'].get('опитування_вік')
        self.pcychiatry = request['custom_fields'].get('запит_психіатр', None)
        print('ManychatRequest', request)
    
    def get_request_tag(self):
        from app.tags.models import Tag
        return Tag.get_by_name(self.tag_name)
    

    def get_specialist(self):
        from app.specialists.models import Specialist
        return Specialist.find_by_tag(self.get_request_tag())




class TextMessage:
    def __init__(self, text, buttons=None):
        self.type = 'text'
        self.text = text
        self.buttons = [] if buttons is None else list(buttons)
        self.json = self.to_json()

    def to_json(self):
        message = {
            'type': self.type,
            'text': self.text,
            'buttons': [self.buttons] if self.buttons else [],
            'parse_mode': 'HTML'
        }
        return message


url = 'https://api.manychat.com/fb/sending/sendContent'
API_TOKEN = '539030:b5bb217ba67cc15f9059df99e175a204'
headers = {
    'Authorization': 'Bearer ' + API_TOKEN,
    'Accept': 'application/json'
}
class ManychatFindSubscriber:
    def __init__(self, manychat_name):
        self.manychat_name = manychat_name
        self.url = 'https://api.manychat.com/fb/subscriber/findByName'

    def get(self, token):
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {'name': self.manychat_name}
        response = requests.get(self.url, params=params, headers=headers)
        
        try:
            response.raise_for_status()  # Check if the request was successful
            response_data = response.json()
            print('Response from ManyChat API:')
            print(response_data)
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        
        return None

    @classmethod
    def get_subscriber_id(cls, manychat_name):
        response_data = cls(manychat_name).get()
        
        if response_data and 'data' in response_data and response_data['data']:
            subscriber_id = response_data['data'][0]['id']
            return subscriber_id
        else:
            print("No subscriber ID found in the response.")
            return None


class ManychatSendMessage():
    version = 'v2'
    content_type = 'telegram'
    message_tag = 'ACCOUNT_UPDATE'

    def __init__(self, subscriber_id, messages):
        self.subscriber_id = subscriber_id
        self.messages = messages
        self.json = self.to_json()

    def to_json(self):
        json = {
            'subscriber_id': self.subscriber_id,
            'data': {
                'version': self.version,
                'content': {
                    'type': self.content_type,
                    'version': self.version,
                    'messages': self.messages
                }
            },
            'message_tag': self.message_tag
        }
        return json
    

    def post(self):
        r = requests.post(url, json=self.json, headers=headers, proxies=None)
        print(r.json())


class ManychatSendFlow:
    def __init__(self, subscriber_id, flow_name):
        self.subscriber_id = subscriber_id
        self.flow_ns = flow_name
        self.url = 'https://api.manychat.com/fb/sending/sendFlow'
        self.json = self.to_json()

    def to_json(self):
        return {
            'subscriber_id': self.subscriber_id,
            'flow_ns': self.flow_ns
        }
    
    def post(self):
        r = requests.post(self.url, json=self.json, headers=headers)




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





class UrlButton:
    def __init__(self, caption: str, url: str):
        self.type = 'url'
        self.caption = caption
        self.url = url
        self.json = self.to_json()


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

    def __init__(self, subscriber_id, data, message_tag, otn_topic_name):
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
        print(r.json())

