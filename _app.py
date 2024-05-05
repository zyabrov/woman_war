from flask import Flask, request, render_template
import _functions
import credentials


app = Flask(__name__)

notion = _functions.Notion(credentials.notion_token)


@app.route('/dateEnd', methods=['POST'])
def date_end():
    manychat_data = request.get_json()
    import datetime
    start_date = manychat_data['dateStart']
    days = manychat_data['days']
    end_date = start_date + datetime.timedelta(days=days)
    print(end_date)
    return {"end_date": end_date}


@app.route('/request_accepted', methods=['POST'])
def manychat_request():
    manychat_data = request.get_json()
    user = _functions.User()
    user.get_manychat_data(manychat_data)
    notion.request_accepted(user.notion_page_id, user.specialist_notion_page_id, user.accepted_date)
    response = {'text': 'request accepted', 'specialist': f'{user.specialist_notion_page_id}', 'user': f'{user.notion_page_id}'}
    print(response)
    return response

@app.route('/updateGroupMessageID', methods=['POST'])
def update_message():
    manychat_data = request.get_json()
    notion_page_id = manychat_data['custom_fields']['notion_page_id']
    message_id = manychat_data['custom_fields']['request_message_id']
    notion.update_group_message_id(notion_page_id, message_id)
    response = {'status': 'ok', 'text': notion.response}
    return response

@app.route('/UpdateSpecialistManychatID', methods=['POST'])
def update_manychat_id():
    manychat_data = request.get_json()
    user = _functions.User()
    user.specialist_manychat_id = manychat_data['id']
    user.page_id = manychat_data['custom_fields']['notion_page_id']
    notion.update_manychat_id(user.page_id, user.specialist_manychat_id)
    response = {'status':'ok', 'notion_page_url': user.notion_page_url}
    return response

@app.route('/UpdateNewSpecialist', methods=['POST'])
def update_specialist():
    manychat_data = request.get_json()
    user = _functions.User()
    user.manychat_id = manychat_data['id']
    user.specialist_page_id = manychat_data['custom_fields']['specialist_notion_page_id']
    user.profile_pic = manychat_data['profile_pic']
    user.name = manychat_data['name']
    user.telegram_username = manychat_data['custom_fields']['telegram_username']
    user.telegram_id = manychat_data['custom_fields']['telegram_id']
    user.specialist_email = manychat_data['custom_fields']['specialist_email']
    notion.update_new_specialist(user)
    response = {'status':'ok', 'notion_page_url': user.notion_page_url}
    return response


@app.route('/zapyt', methods=["GET"])
def index():
    print("get checkbox request")
    # Отримати значення параметру з GET-запиту
    user_id = request.args.get('user_id')
    print('page_id from request', user_id)
    return render_template("zapyt.html", subscriber_id = user_id)

@app.route("/submit", methods=["POST"])
def submit():
    selected_options = request.form.getlist("option")
    selected_options_text = "; ".join(selected_options)
    page_id = request.form.get('page_id')
    print(selected_options)
    notion.update_zapyt(page_id, selected_options_text)
    return "Ваш запит прийнято. Очікуйте підтвердження спеціалістом"


"""
@app.route("/test_manychat", methods=["GET", "POST"])
def test_manychat():
    url = "https://api.manychat.com/fb/subscriber/setCustomField"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer 539030:b5bb217ba67cc15f9059df99e175a204",
        "Content-Type": "application/json"
    }
    data = {
        "subscriber_id": 61796569,
        "field_id": 8792646,
        "field_value": "Не знаю як далі заробляти"
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.text)



# Задайте токен доступу до Manychat API тут
access_token = 'Bearer 539030:b5bb217ba67cc15f9059df99e175a204'

# Задайте ім'я поля в Manychat, де будуть зберігатися опції
field_name = 'запит_як_дізналися'

@app.route('/submit', methods=['POST'])
def submit():
    subscriber_id = request.form['subscriber_id']
    options = request.form.getlist('option')
    options_str = ', '.join(options)
    url = 'https://api.manychat.com/fb/subscriber/setCustomFieldByName'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    data = {'subscriber_id': subscriber_id, 'field_name': field_name, 'field_value': options_str}
    response = requests.post(url, headers=headers, json=data)
    print(jsonify({'status': response.status_code}))
    return jsonify({'status': response.status_code})

@app.route('/save-data', methods=['POST'])
def save_data():
    # Отримуємо дані, що були передані з форми
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    option5 = request.form.get('option5')

    # Тут ми можемо зберегти отримані дані в базу даних, файл або відправити їх до ManyChat через API

    # Повертаємо користувача на сторінку з формою або на іншу потрібну сторінку
    return redirect('/success')
"""

@app.route('/', methods=['GET'])
def test():
    print('Get request')



@app.route('/notion', methods=['GET', 'POST'])
def notion_request(user):
    pass