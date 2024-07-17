from app.requests import bp
from app.requests.models import Request
from flask import render_template, redirect, url_for, request


@bp.route("/", methods=["GET", "POST"])
def requests():
    return render_template("requests.html", requests = Request.query.all())


@bp.route('/free', methods=['POST'])
def free_request():
    from app.manychat.models import ManychatRequest
    from app.users.models import User
    manychat_request = ManychatRequest(request.get_json())
    user = User.get_and_update_or_create_from_request(manychat_request)
    print('\n\n----------------\n')
    print('free request user: ', user)
    r = Request.add_from_request(manychat_request)
    print('new free request: ', r)
    if r:
        return {'status': '200', 'user_age': r.user_age}
    else:
        return {'status': '404'}


@bp.route('/free/group', methods=['POST'])
def free_request_group():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request.get_json())
    r = Request.add_from_request(manychat_request)
    if r:
        return {'status': '200'}
    else:
        return {'status': '404'}
    

@bp.route('/save_message_id', methods=['POST'])
def save_message_id():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request.get_json())
    r = Request.get(manychat_request.id)
    if r:
        r.save_message_id(manychat_request.message_id)
        return {'status': '200'}
    else:
        return {'status': '404'}


@bp.route('/accept', methods=['POST'])
def accept_request():
    from app.manychat.models import ManychatRequest
    from app.telegram.models import UpdateMessage, free_group_id
    from app.specialists.models import Specialist
    from app.manychat.models import TextMessage, ManychatSendMessage
    
    manychat_request = ManychatRequest(request.get_json())
    specialist = Specialist.get(manychat_request.user_id)
    print('\n\n----------------\n')
    print('specialist: ', specialist)
    print('user request id: ', manychat_request.user_request_id)
    if not specialist:
        specialist = Specialist.add(
            name=manychat_request.manychat_username, 
            manychat_id=manychat_request.user_id,
            manychat_username=manychat_request.manychat_username,
            telegram_username=manychat_request.username,
            phone=manychat_request.phone,
            manychat_img=manychat_request.manychat_img
        )
        print('new specialist: ', specialist)

    r = Request.get(int(manychat_request.user_request_id))
    print('request:', r)
    r.add_specialist(specialist.id)

    #edit the group message
    message_id = int(r.message_id)
    message_text = f'Запит {r.id} прийняв спеціаліст @{specialist.telegram_username}'
    update_message = UpdateMessage(free_group_id, message_id, message_text)
    update_message_response = update_message.post()

    #message to the user
    user_message = TextMessage(f'Ваш запит прийняв спеціаліст: {specialist.name} @{specialist.telegram_username}')
    send_message = ManychatSendMessage(r.user_id, messages=[user_message.json])
    send_message.post()

    #message to the specialist
    specialist_message = TextMessage(
        f'''Запит {r.id} від {r.user_full_name} (@{r.user_username}) прийнятий. 

        Запит:{r.request_name}
        Вік: {r.user_age}
        Дата народження: {r.user_birthdate}
        Де знаходиться: {r.user_where_is} - {r.user_where_is_city}
        Попереднй досвід з психологом: {r.user_worked_with_psychologist_before}
        Телефон: {r.user_phone}
        Як дізналися: {r.user_how_known}''')
    send_message = ManychatSendMessage(specialist.id, messages=[specialist_message.json])
    send_message.post()

    return {'status': '200', 'update_message_response': update_message_response}


@bp.route('/new_find_specialists_request', methods=['POST'])
def find_specialists_request(): 
    from app.manychat.models import ManychatRequest
    request_data = request.get_json()
    print('/n/n----------------/n')
    print('request_data: ', request_data)
    manychat_request = ManychatRequest(request_data)
    
    from app.users.models import User
    user = User.get_and_update_or_create_from_request(manychat_request)
    if user:
        print('/n/n----------------/n')
        print('user founded: ', user)
    
        r = Request.add_from_request(manychat_request)
        if r:
            print('/n/n----------------/n')
            print('request founded: ', r)
            from app.specialists.models import Specialist
            specialists = Specialist.find_by_tag(manychat_request.get_request_tag())

            if specialists:
                print('/n/n----------------/n')
                print('specialists founded: ', specialists)
                specialists_number = len(specialists)
                return {'status': '200', 'specialists': specialists_number, 'message':'Знайдено спеціалістів: ' + str(specialists_number)}
            else:
                message = 'Спеціалістів не знайдено'
            
        else:
            print('/n/n----------------/n')
            print('no request found')
            message = 'Запит не знайдено'

    else:
        print('/n/n----------------/n')
        print('no user found')
        message = 'Користувача не знайдено'

    return {'status': '404', 'specialists': 0, 'message': message}


@bp.route('/request_card/<int:request_id>', methods=['GET'])
def request_card(request_id):
    r = Request.get(request_id)
    return render_template('request_card.html', request=r)



@bp.route('/delete_request/<int:request_id>', methods=['GET', 'POST'])
def delete_request(request_id):
    r = Request.get(request_id)
    r.delete()
    return redirect(url_for('requests.requests'))


@bp.route('/get_feedback/<int:request_id>', methods=['POST'])
def get_feedback(request_id):
    r = Request.get(request_id)
    if r:
        from app.users.models import User
        user = User.get(r.user_id)
        if user:
            from app.manychat.models import ManychatSendFlow
            #send flow to the user
            send_flow = ManychatSendFlow(r.user_id, 'content20240704084420_085880')
            send_flow.post()
            return 'Запит відправлено'

    return {'status': '404'}
           

    

