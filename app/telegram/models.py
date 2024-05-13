import requests

BOT_TOKEN = '5976923303:AAFlyJjx7QAjWlKNlxDENLAHlmW2T1eAoUE'
headers = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
base_url = "https://api.telegram.org/bot" + BOT_TOKEN
paid_group_id = -4179064257
free_group_id = -1001342499881
    


class SendMessage():    
    def __init__(self, chat_id, text, keyboard=None):
        self.chat_id = chat_id
        self.text = text
        self.keyboard = keyboard
        self.url = base_url + "/sendMessage"
        self.json = self.to_json()


    def to_json(self):
        json = {
            "chat_id": self.chat_id,
            "text": self.text,
            "disable_notification": False, 
            "parse_mode": "HTML"
        }
        if self.keyboard:
            json["reply_markup"] = self.keyboard
        return json
    

    def post(self):
        r = requests.post(self.url, json=self.json, headers=headers)
        r.raise_for_status()
        print(r.json())
    
    
class UpdateMessage():
    def __init__(self, chat_id, message_id, text, keyboard=None):
        self.url = base_url + "/editMessageText"
        self.chat_id = chat_id
        self.message_id = message_id
        self.text = text
        self.keyboard = keyboard
        self.json = self.to_json()

    def to_json(self):
        json = {
            "chat_id": self.chat_id,
            "message_id": self.message_id,
            "text": self.text,
            "disable_notification": False, 
            "parse_mode": "HTML"
        }
        if self.keyboard:
            json["reply_markup"] = self.keyboard
        return json
    
    def post(self):
        r = requests.post(self.url, json=self.json, headers=headers)
        r.raise_for_status()
        print(r.json())


    
    