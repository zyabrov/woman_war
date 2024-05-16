from app.requests import bp
from app.requests.models import Request
from flask import render_template, redirect, url_for, request


@bp.route("/", methods=["GET", "POST"])
def requests():
    return render_template("requests.html", requests = Request.query.all())


@bp.route('/free', methods=['POST'])
def free_request():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request.get_json())
    r = Request.add_from_request(manychat_request)
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
    manychat_request = ManychatRequest(request.get_json())
    r = Request.get(manychat_request.id)
    if r:
        from app.specialists.models import Specialist
        specialist = Specialist.get(manychat_request.user_id)
        if specialist:
            r.add_specialist(specialist.id)

            #edit the group message
            from app.telegram.models import UpdateMessage, free_group_id
            message_id = int(r.message_id)
            message_text = f'Запит {r.id} прийняв спеціаліст {specialist.telegram_username}'
            update_message = UpdateMessage(free_group_id, message_id, message_text)
            update_message.post()

            from app.manychat.models import TextMessage, ResponseContent, SendContent
            #message to the user
            user = r.user
            user_message = TextMessage(f'Ваш запит прийняв спеціаліст: {specialist.name}')
            send_content = SendContent(user.id, ResponseContent(msg_type='telegram', messages=[user_message.json]))
            send_content.post()

            #message to the specialist
            specialist_message = TextMessage(f'Запит {r.id} від {user.name} прийнятий./nПовідомлення клієнту надісано./n/nДані запиту: /nЗапит:{r.tag}\nВік: {r.user.age}\nДата народження: {r.user.birthdate}\nДе знаходиться: {r.user.where_is} - {r.user.where_is_city}\nПопереднй досвід з психологом: {r.user.worked_with_psychologist_before}\nТелефон: {r.user.phone}\nЯк дізналися: {r.user.how_known}')
            send_content = SendContent(specialist.id, ResponseContent(msg_type='telegram', messages=[specialist_message.json]))
            send_content.post()

            return {'status': '200'}
        else:
            print('specialist not founded')
            return {'status': '404'}
    else:
        print('request not founded')
        return {'status': '404'}


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

