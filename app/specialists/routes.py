from flask import render_template, Blueprint, request
from app.specialists import bp
from app.specialists.models import Specialist
from app.specialists.forms import NewSpecialistForm


@bp.route('/', methods=['GET', 'POST'])
def specialists():
    return render_template('specialists.html', specialists=Specialist.query.all())


@bp.route('/<int:specialist_id>', methods=['GET', 'POST'])
def specialist_card(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        return render_template('specialist_card.html', specialist=specialist)
        

@bp.route('/new_specialist', methods=['GET', 'POST'])
def new_specialist():
    form = NewSpecialistForm(request.form)

    if form.validate_on_submit():
        new_specialist = Specialist.add(form)
        return render_template('specialists.html', specialists=Specialist.query.all())
    
    return render_template('new_specialist.html', form=form)


@bp.route('/edit_specialist/<int:specialist_id>', methods=['GET', 'POST'])
def edit_specialist(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        form = NewSpecialistForm(request.form, obj=specialist)
    
        if form.validate_on_submit():
            specialist.edit(form)
            return render_template('specialists.html', specialists=Specialist.query.all())
        return render_template('edit_specialist.html', form=form, specialist=specialist)
    

@bp.route('/delete_specialist/<int:specialist_id>', methods=['GET', 'POST'])
def delete_specialist(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        specialist.delete()
        return render_template('specialists.html', specialists=Specialist.query.all())



@bp.route('/find_request/<int:request_id>', methods=['GET'])
def find_request(request_id):
    specialists = Specialist.find_by_request_id(request_id)
    return render_template('specialists_cards.html', specialists=specialists, request_id=request_id)


@bp.route('/choose/<int:request_id>/<int:specialist_id>', methods=['GET'])
def choose(request_id, specialist_id):
    specialist = Specialist.query.get(specialist_id)
    
    #update request
    from app.requests.models import Request
    request = Request.query.get(request_id)
    request.add_specialist(specialist_id)

    #message to the user
    from app.manychat.models import TextMessage, ResponseContent, SendContent
    user_message = TextMessage(f'Ваш запит надісланий спеціалісту: {specialist.name}')
    user_content = ResponseContent(msg_type='telegram', messages=[user_message.to_json()])
    send_content = SendContent(request.user.id, user_content.to_json(), 'ACCOUNT_UPDATE', 'Request has been sent')
    send_content.post()

    #message to the specialist
    from app.manychat.models import TextMessage, ResponseContent, SendContent
    specialist_message = TextMessage(f'{request.user.name} обрав вас для запиту:\n{request.tag}\n\nІнформація запиту:\nВік: {request.user.age}\nДата народження: {request.user.birthdate}\nДе знаходиться: {request.user.where_is} - {request.user.where_is_city}\nПопереднй досвід з психологом: {request.user.worked_with_psychologist_before}\nТелефон: {request.user.phone}\nЯк дізналися: {request.user.how_known}')
    specialist_content = ResponseContent(msg_type='telegram', messages=[specialist_message.to_json()])
    send_content = SendContent(specialist.id, specialist_content.to_json(), 'ACCOUNT_UPDATE', 'New Request').post()
    send_content.post()
    
    return 'Запит надіслано спеціалісту'
    