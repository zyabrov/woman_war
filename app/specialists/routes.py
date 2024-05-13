from flask import render_template, redirect, url_for, request
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
        return redirect(url_for('specialists.specialists'))



@bp.route('/find_request/<int:request_id>', methods=['GET'])
def find_request(request_id):
    specialists = Specialist.find_by_request_id(request_id)
    return render_template('specialists_cards.html', specialists=specialists, request_id=request_id)


@bp.route('/choose/<int:request_id>/<int:specialist_id>', methods=['GET'])
def choose(request_id, specialist_id):
    specialist = Specialist.query.get(specialist_id)
    
    #update request
    from app.requests.models import Request
    r = Request.query.get(request_id)
    r.add_specialist(specialist_id)

    from app.manychat.models import TextMessage, ManychatSendMessage, UrlButton
    #message to the user
    user_message = TextMessage(f'Ваш запит надісланий спеціалісту: {specialist.name}')
    send_message = ManychatSendMessage(r.user.id, messages=[user_message.json])
    send_message.post()

    #message to the specialist
    user_telegram_username = r.user.username
    specialist_message_btn = None
    if user_telegram_username:
        specialist_message_btn = UrlButton(caption='Написати', url='https://t.me/').json
    specialist_message = TextMessage(f'{r.user.name} обрав вас для запиту\n\nТег запиту: {r.tag}\nВік: {r.user.age}\nДата народження: {r.user.birthdate}\nДе знаходиться: {r.user.where_is} - {r.user.where_is_city}\nПопереднй досвід з психологом: {r.user.worked_with_psychologist_before}\nТелефон: {r.user.phone}\nЯк дізналися: {r.user.how_known}', buttons=[specialist_message_btn])
    send_message = ManychatSendMessage(specialist.id, messages=[specialist_message.json])
    send_message.post()

    #message to the group
    from app.telegram.models import SendMessage, paid_group_id
    group_message = SendMessage(paid_group_id, f'Платний запит № {r.id}: {r.tag}. Спеціаліст: {specialist.name}')
    group_message.post()

    return 'Запит надіслано спеціалісту'
    