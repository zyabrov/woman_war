from flask import Blueprint, request
from app.manychat import bp
from app.manychat.models import ManychatRequest, TextMessage, UrlButton, Response, ResponseContent, SendContent, ImageMessage



@bp.route('/find_specialists', methods=['POST'])
def find_specialist():
    manychat_request = ManychatRequest(request)
    from app.specialists.models import Specialist
    from app.requests.models import Request
    from app.users.models import User
    user = User.get_and_update_or_create_from_request(manychat_request)
    print('/n/n----------------/n')
    print('user: ', manychat_request.user_id)
    new_request = Request.add_from_request(manychat_request)
    print('request: ', new_request)

    messages = []
    server_url = 'http://127.0.0.1:5000'
    specialists = Specialist.find_by_tag(manychat_request.get_request_tag())
    if specialists:
        print('specialists: ', specialists)
        for specialist in specialists:
            btn1 = UrlButton(caption='ℹ️ Резюме', url=f"{specialist.cv}")
            btn2 = UrlButton(caption='✅ Обрати', url=f"{server_url}/manychat/specialists/choose/{new_request.id}/{specialist.id}")
            text_message = TextMessage(f'<b>{specialist.name}</b>/n{specialist.description}', buttons=[btn1, btn2])
            image_message = ImageMessage(specialist.image)
            messages.append(image_message.to_json())
            messages.append(text_message.to_json())
    else:
        message = TextMessage('Спеціалістів не знайдено')
        messages.append(message)
    
    print('messages: ', messages)
    response_content = ResponseContent(msg_type='telegram', messages=messages).to_json()
    response = Response(response_content)
    print('\n\n----------------/n')
    print('response: ', response)
    return response.to_json()


@bp.route('/specialists/<int:request_id>/<int:specialist_id>', methods=['POST'])
def choose_specialist(request_id, specialist_id):
    from app.specialists.models import Specialist
    specialist = Specialist.query.get(specialist_id)
    messages = []
    server_url = 'http://127.0.0.1:5000'
    if specialist:
        messages.append(
            TextMessage(
                f"{specialist.name}/n{specialist.description}",
                [
                    UrlButton(caption='✅ Обрати', url=f"{server_url}/manychat/specialists/choose/{request_id}/{specialist.id}").to_json()
                    ]
            ).to_json()
        )
        
    response_content = ResponseContent(msg_type='telegram', messages=messages).to_json()
    response = Response(response_content)
    return response.to_json()


@bp.route('/specialists/choose/<int:request_id>/<int:specialist_id>', methods=['POST'])
def choose_request(request_id, specialist_id):
    
    from app.specialists.models import Specialist
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        from app.requests.models import Request
        request = Request.query.get(request_id)
        request.add_specialist(specialist.id)

        #message to the specialist
        specialist_message = TextMessage(f'{request.user.name} обрав вас для запиту:\n{request.tag}\n\nІнформація запиту:\nВік: {request.user.age}\nДата народження: {request.user.birthdate}\nДе знаходиться: {request.user.where_is} - {request.user.where_is_city}\nПопереднй досвід з психологом: {request.user.worked_with_psychologist_before}\nТелефон: {request.user.phone}\nЯк дізналися: {request.user.how_known}').to_json
        specialist_content = ResponseContent(msg_type='telegram', messages=[specialist_message]).to_json()
        SendContent(specialist.id, specialist_content, 'ACCOUNT_UPDATE', 'New Request').post()
        
        #message to the user
        user_message = TextMessage('Ваш запит надісланий спеціалісту').to_json
        user_content = ResponseContent(msg_type='telegram', messages=[user_message]).to_json
        SendContent(request.user.id, user_content, 'ACCOUNT_UPDATE', 'Request has been sent').post()
        return {"status": 200, 'message': {"specialist": {"name": specialist.name, "id": specialist.id}}}
    else:
        return {'status': 404, 'message': {'Спеціаліста не знайдено'}}
