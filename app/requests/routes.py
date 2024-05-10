from flask import render_template, redirect, url_for, request
from app.requests import bp
from app.requests.models import Request


@bp.route("/", methods=["GET", "POST"])
def requests():
    return render_template("requests.html", requests = Request.query.all())


@bp.route('/free', methods=['POST'])
def free_request():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request)
    request = Request.add_from_request(manychat_request, 'free')
    if request:
        return {'status': '200'}
    else:
        return {'status': '404'}
    

@bp.route('/accept/<int:request_id>', methods=['GET'])
def accept_request(request_id):
    print('/n/n----------------/n')
    print('accept_request: ', request)
    print('accept_request form: ', request.form)
    print('accept_request data: ', request.data)
    from app.specialists.models import Specialist
    specialist = Specialist.find_by_telegram_username(request.form['callback_query']['from']['username'])
    if specialist:
        r = r.query.get(request_id)
        r.add_specialist(specialist.id)

        #edit the group message
        bot_token = '5976923303:AAFlyJjx7QAjWlKNlxDENLAHlmW2T1eAoUE'
        base_url = f'https://api.telegram.org/bot{bot_token}/'
        message_id = request.form['callback_query']['message']['message_id']
        message_text = request.form['callback_query']['message']['text']
        edit_message_url = f'{base_url}editMessageText'
        edit_params = {
            'chat_id': request.form['callback_query']['message']['chat']['id'],
            'message_id': message_id,
            'text': message_text,
            'reply_markup': None,
            'parse_mode': 'HTML'
        }
        response = requests.post(edit_message_url, json=edit_params)
        print(response.json())

        from app.manychat.models import TextMessage, ResponseContent, SendContent
        #message to the user
        user = r.user
        user_message = TextMessage(f'Ваш запит прийняв спеціаліст: {specialist.name}')
        send_content = SendContent(user.id, ResponseContent(msg_type='telegram', messages=[user_message.json]))
        send_content.post()

        #message to the specialist
        specialist_message = TextMessage(f'Запит {r.id}від {user.name} прийнятий./nПовідомлення клієнту надісано./n/nДані запиту: /nЗапит:{r.tag}\nВік: {r.user.age}\nДата народження: {r.user.birthdate}\nДе знаходиться: {r.user.where_is} - {r.user.where_is_city}\nПопереднй досвід з психологом: {r.user.worked_with_psychologist_before}\nТелефон: {r.user.phone}\nЯк дізналися: {r.user.how_known}')
        send_content = SendContent(specialist.id, ResponseContent(msg_type='telegram', messages=[specialist_message.json]))
        send_content.post()

        return {'status': '200'}
    else:
        return {'status': '404'}


@bp.route('/find_specialists', methods=['POST'])
def find_specialists():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request)
    
    from app.users.models import User
    User.get_and_update_or_create_from_request(manychat_request)
    
    Request.add_from_request(manychat_request, 'paid')

    from app.specialists.models import Specialist
    specialists = Specialist.find_by_tag(manychat_request.get_request_tag())

    if specialists:
        specialists_number = len(specialists)
        return {'status': '200', 'specialists': specialists_number}
    else:
        return {'status': '404', 'specialists': 0}


@bp.route('/request_card/<int:request_id>', methods=['GET'])
def request_card(request_id):
    request = Request.query.get(request_id)
    return render_template('request_card.html', request=request)



@bp.route('/delete_request/<int:request_id>', methods=['GET', 'POST'])
def delete_request(request_id):
    request = Request.query.get(request_id)
    request.delete()
    return redirect(url_for('requests.requests'))

