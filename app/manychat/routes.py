from flask import Blueprint, request
from app.manychat import bp
from app.manychat.models import ManychatRequest, TextMessage, UrlButton, Response



@bp.route('/find_specialists', methods=['POST'])
def find_specialist():
    manychat_request = ManychatRequest(request)
    from app.specialists.models import Specialist
    from app.tags.models import Tag
    tag = Tag.get_by_name(manychat_request.tag)
    print('tag', tag)
    specialists = Specialist.find_by_tag(tag)
    from app.requests.models import Request
    from app.users.models import User
    user = User.get_or_create(manychat_request.user_id, manychat_request.full_name)
    print('/n/n----------------/n')
    print('user: ', manychat_request.user_id)
    print('tag: ', tag)
    new_request = Request.add(manychat_request.id, user.id, tag.id)
    print('request: ', new_request)

    messages = []
    server_url = 'http://127.0.0.1:5000'
    if specialists:
        print('specialists: ', specialists)
        for specialist in specialists:
            btn1 = UrlButton('ℹ️ Інфо', f"{server_url}/manychat/specialists/{specialist.id}')")
            btn2 = UrlButton('✅ Обрати', f"{server_url}/manychat/specialists/choose/{specialist.id}')")
            message = TextMessage(f'{specialist.name}', buttons=[btn1, btn2])
            messages.append(message)
    else:
        message = TextMessage('Спеціалістів не знайдено')
        messages.append(message)
    
    print('messages: ', messages)
    response = Response(msg_type='telegram', messages=messages)
    print('\n\n----------------/n')
    print('response: ', response)
    return response.to_json()


@bp.route('/specialists/<int:specialist_id>', methods=['POST'])
def choose_specialist(specialist_id):
    manychat_request = ManychatRequest(request)
    from app.specialists.models import Specialist
    specialist = Specialist.query.get(specialist_id)
    messages = []
    server_url = 'http://127.0.0.1:5000'
    if specialist:
        messages.append(
            TextMessage(
                f"{specialist.name}/n{specialist.description}",
                [
                    UrlButton('✅ Обрати', f"{server_url}/manychat/specialists/choose/{specialist.id}')").to_json()
                    ]
            ).to_json()
        )
    return Response(
        type='telegram',
        messages=messages
    ).to_json()


@bp.route('/specialists/choose/<int:specialist_id>', methods=['POST'])
def choose_request(specialist_id):
    manychat_request = ManychatRequest(request)
    from app.specialists.models import Specialist
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        from app.requests.models import Request
        request = Request.query.get(manychat_request.id)
        request.add_specialist(specialist)
        return {"status": 200, "specialist": {"name": specialist.name, "id": specialist.id}}
    else:
        return '404'
