import requests


class User:
    def __init__(self):
        self.tg_id = None
        self.tg_username = None
        self.notion_page_id = None
        self.specialist_notion_id = None
        self.manychat_data = None
        self.notion_page_url = None

    def get_manychat_data(self, manychat_data):
        self.manychat_data = manychat_data
        self.tg_id = self.manychat_data['custom_fields']['запит_telegram_id']
        self.tg_username = self.manychat_data['custom_fields']['запит_telegram_username']
        self.notion_page_id = self.manychat_data['custom_fields']['запит_notion_page_id']
        print(self.notion_page_id)
        self.phone = self.manychat_data['phone']
        self.specialist_notion_page_id = self.manychat_data['custom_fields']['specialist_notion_page_id']
        print(self.specialist_notion_page_id)
        self.accepted_date = self.manychat_data['custom_fields']['Коли прийнятий запит']



    def get_manychat_value(self, field, iscustom):
        value = None
        if iscustom == True:
            value = self.manychat_data['custom_fields'][field]
        else:
            value = self.manychat_data[field]
        return value


class Specialist:
    tags = []
    page_id = None


    def __init__(self, notion_page_id=None):
        self.page_id = notion_page_id

    @classmethod
    def get_by_tag(self, tag):
        pass




class Admin(User):
    def __init__(self, user_id):
        super.__init__(self,user_id)



class Notion:
    def __init__(self, notion_token):
        self.url = None
        self.token = notion_token
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            'Authorization': f"Bearer {self.token}"
        }
        self.json = None
        self.response = None
        self.page_id = None
        self.sessions_db_id = '2c29d368336d4361a992dd6558957786'


    def get_page(self, page_id):
        url = f'https://api.notion.com/v1/pages/{page_id}'
        response = requests.get(url, headers=self.headers)
        print(response.text)


    def request_accepted(self, page_id, specialist_notion_page_id, accepted_date):
        self.page_id = page_id
        self.specialist_notion_page_id = specialist_notion_page_id
        self.accepted_date = accepted_date
        self.json = {
            'properties': {
                "Статус клієнта": { "status": "Запит прийнято" },
                "Спеціаліст": { "relation": [{ "id": self.specialist_notion_page_id }] },
                "Коли прийнятий": {"date": { "start": self.accepted_date}}
                }
            }
        self.update_page_properties()
        """
        self.create_sessions()
        """
        print("new request accepted")


    def create_sessions(self):
        self.json = {
            "parent": { "database_id": self.sessions_db_id },
            "properties": {
                "title": { "title": [{ "text": {"content": "1"} }] },
                "Клієнт": { "relation": [{ "id": self.page_id }] },
                }
            }
        self.create_page()
        print("session page created")


    def update_new_specialist(self, user):
        self.page_id = user.specialist_page_id
        print(self.page_id)
        self.json = {
            'cover': { "external": { "url": user.profile_pic } },
            'properties': {
                "Manychat ID": { "number": int(user.manychat_id) },
                "ПІБ (заповнюється автоматично)": { "title": [{ "text": {"content": user.name} }] },
                "telegram_id": { "rich_text": [{ "text": {"content": user.telegram_id} }] },
                "telegram_username": { "rich_text": [{ "text": { "content": user.telegram_username} }] },
                "profile_pic": {"files": [{ "external": { "url": user.profile_pic }, "name": user.name + "profile_pic.jpg" }] }
                }
            }
        self.update_page_properties()



    def update_manychat_id(self, page_id, manychat_id):
        self.page_id = page_id
        self.manychat_id = int(manychat_id)
        self.json = {
            "properties": {
                "Manychat ID": { "type": "number", "number": self.manychat_id }
                }
            }
        self.update_page_properties()

    def update_zapyt(self, page_id, text):
        self.page_id = page_id
        self.json = {
            "properties": {
                "Запит": {"type": "rich_text", "rich_text": [{
                    "text": {"content": text}
                    }]}
                }
            }
        self.update_page_properties()

    def update_group_message_id(self, page_id, message_id):
        self.page_id = page_id
        self.group_message_id = message_id
        self.json = {
            "properties":{
                "telegram_group_message_id": {
                    "rich_text": [{
                        "text": {"content": self.group_message_id}
                        }]
                    }
                }
            }
        self.update_page_properties()


    def update_page_properties(self):
        url = f"https://api.notion.com/v1/pages/{self.page_id}"
        response = requests.patch(url, json=self.json, headers=self.headers)
        self.data = response.json()
        if self.data is not None:
            self.response = "page updated"
        else:
            self.response = "error"

    def create_page(self):
        url = "https://api.notion.com/v1/pages"
        response = requests.post(url, json=self.json, headers=self.headers)
        self.data = response.json()
        print(self.data)


