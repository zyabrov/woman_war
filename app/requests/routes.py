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
    Request.add_from_request(manychat_request, 'free')
    return {'status': '200'}


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
        return {'status': '200', 'specialists': len(specialists)}
    else:
        return {'status': '404', 'specialists': 0}


@bp.route('/choose/<int:request_id>/<int:specialist_id>', methods=['GET'])
def specialist_choose(request_id, specialist_id):
    from app.specialists.models import Specialist
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        request = Request.query.get(request_id)
        request.add_specialist(specialist.id)

        #message to the specialist
        from app.manychat.models import TextMessage, ResponseContent, SendContent
        specialist_message = TextMessage(f'{request.user.name} обрав вас для запиту:\n{request.tag}\n\nІнформація запиту:\nВік: {request.user.age}\nДата народження: {request.user.birthdate}\nДе знаходиться: {request.user.where_is} - {request.user.where_is_city}\nПопереднй досвід з психологом: {request.user.worked_with_psychologist_before}\nТелефон: {request.user.phone}\nЯк дізналися: {request.user.how_known}').to_json
        specialist_content = ResponseContent(msg_type='telegram', messages=[specialist_message]).to_json()
        SendContent(specialist.id, specialist_content, 'ACCOUNT_UPDATE', 'New Request').post()

        #message to the user
        user_message = TextMessage(f'Ваш запит надісланий спеціалісту {specialist.name}').to_json
        user_content = ResponseContent(msg_type='telegram', messages=[user_message]).to_json
        SendContent(request.user.id, user_content, 'ACCOUNT_UPDATE', 'Request has been sent').post()

        return 'Запит надіслано спеціалісту'
    else:
        return 'Спеціаліста не знайдено'


@bp.route('/request_card/<int:request_id>', methods=['GET'])
def request_card(request_id):
    request = Request.query.get(request_id)
    return render_template('request_card.html', request=request)



@bp.route('/delete_request/<int:request_id>', methods=['GET', 'POST'])
def delete_request(request_id):
    request = Request.query.get(request_id)
    request.delete()
    return redirect(url_for('requests.requests'))

