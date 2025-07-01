from flask import render_template, redirect, url_for, request
from app.specialists import bp
from app.specialists.models import Specialist
from app.specialists.forms import NewSpecialistForm, EditSpecialistForm


@bp.route('/', methods=['GET', 'POST'])
def specialists():
    return render_template('specialists.html', specialists=Specialist.query.all())


@bp.route('/<int:specialist_id>', methods=['GET', 'POST'])
def specialist_card(specialist_id):
    specialist = Specialist.get(specialist_id)
    if specialist:
        return render_template('specialist_card.html', specialist=specialist)
        

@bp.route('/new_specialist', methods=['GET', 'POST'])
def new_specialist():
    print('/n/n----------------/n')
    print('new_specialist request: ', request.form)
    form = NewSpecialistForm()
    selected_tags = None

    if form.validate_on_submit():
        selected_tags = form.tags_select.data
        print('/n/n----------------/n')
        print('selected_tags: ', selected_tags)
        from app.manychat.models import ManychatFindSubscriber
        subscriber_finder = ManychatFindSubscriber(form.manychat_username_input.data)
        access_token = "539030:b5bb217ba67cc15f9059df99e175a204"
        response_data = subscriber_finder.get(access_token)
        print('/n/n----------------/n')
        print('response_data: ', response_data)
        
        manychat_id = response_data.get('data')[0]['id']
        for field in response_data['data'][0]['custom_fields']:
            if field['name'] == 'telegram_username':
                telegram_username = field['value']
            if field['name'] == 'phone':
                phone = field['value']

        if manychat_id:
            print('/n/n----------------/n')
            print('specialist manychat_id: ', manychat_id)
            new_specialist = Specialist.add(
                name=form.name.data,
                manychat_id=manychat_id,
                manychat_username=form.manychat_username_input.data,
                telegram_username=telegram_username,
                phone=phone,
                description=form.description.data,
                cv=form.cv.data,
                tags=selected_tags,
                cost=form.cost.data,
                manychat_img=response_data['data'][0].get('profile_pic')
            )
            if new_specialist:
                print('new_specialist: ', new_specialist)
                return redirect(url_for('specialists.specialists'))
            else:
                print('new_specialist error')
        else:
            print('manychat_id error')
    
    return render_template('new_specialist.html', form=form, selected_tags=selected_tags)


@bp.route('/add_specialist/free', methods=['POST'])
def new_specialist_free():
    from app.manychat.models import ManychatRequest
    manychat_request = ManychatRequest(request.get_json())
    specialist = Specialist.get(manychat_request.user_id)
    if not specialist:
        specialist = Specialist.add_free(manychat_request.user_id, manychat_request.manychat_username, manychat_request.username)
        if specialist:
            print('/n/n----------------/n')
            print('new_specialist: ', specialist)
            message = 'Specialist was added'
            return {'status': '200', 'message': message}
        else:
            print('/n/n----------------/n')
            print('new_specialist error')
            message = 'Specialist was not added'
            return {'status': '500', 'message': message}
    else:
        print('/n/n----------------/n')
        print('specialist already exists')
        message = 'Specialist already exists'
        return {'status': '200', 'message': message}


@bp.route('/edit_specialist/<int:specialist_id>', methods=['GET', 'POST'])
def edit_specialist(specialist_id):
    specialist = Specialist.get(specialist_id)
    if specialist:
        form = EditSpecialistForm(
            name_input=specialist.name,
            tg_username=specialist.telegram_username,
            description_input=specialist.description,
            phone=specialist.phone,
            id=specialist.id
        )
        return render_template('edit_specialist.html', form=form, specialist=specialist)
    

@bp.route('/update_specialist', methods=['POST'])
def update_specialist():
    form = EditSpecialistForm(request.form)
    specialist = Specialist.get(form.id.data)
    if specialist:
        specialist.update(form)
    return redirect(url_for('specialists.specialists'))
    

@bp.route('/delete_specialist/<int:specialist_id>', methods=['GET', 'POST'])
def delete_specialist(specialist_id):
    specialist = Specialist.get(specialist_id)
    if specialist:
        specialist.delete()
        return redirect(url_for('specialists.specialists'))



@bp.route('/find_request/<int:request_id>', methods=['GET'])
def find_request(request_id):
    from app.requests.models import Request
    r = Request.get(request_id)
    if r:
        print('find_request: ', r)
        specialists = Specialist.find_by_request_id(r.id)
        if specialists:
            return render_template('specialists_cards.html', specialists=specialists, request_id=request_id) 
        else:
            print('specialists not found')
            error = 'Спеціалістів не знайдено'
            return redirect(url_for('main.error'), error)
    else:
        print('request not found')
        error = 'Запит не знайдено'
    return redirect(url_for('main.error'), error)


@bp.route('/choose/<int:request_id>/<int:specialist_id>', methods=['GET'])
def choose(request_id, specialist_id):
    specialist = Specialist.get(specialist_id)

    if specialist:
        print('/n/n----------------/n')
        print('choose: ', specialist)
        #update request
        from app.requests.models import Request
        r = Request.get(request_id)

        if r:
            print('request: ', r)
            r.add_specialist(specialist_id)
            from app.manychat.models import TextMessage, ManychatSendMessage, UrlButton
            user = r.user

            if user:
                print('user: ', user)  
                
                #message to the user
                user_message = TextMessage(f'Ваш запит надісланий спеціалісту: {specialist.name}')
                ManychatSendMessage(user.id, messages=[user_message.json]).post()
                # message to the group
                from app.telegram.models import SendMessage, paid_group_id
                text = f'Платний запит № {r.id}: {r.tag}. Спеціаліст: {specialist.name} @{specialist.telegram_username}\n\nТег запиту: {r.tag}\n\nВік: {r.user.age}\nДата народження: {r.user.birthdate}\nДе знаходиться: {r.user.where_is} - {r.user.where_is_city}\nПопереднй досвід з психологом: {r.user.worked_with_psychologist_before}\nЯк дізналися: {r.user.how_known}\n\nТелефон: {r.user.phone}\nЛогін Телеграм: @{r.user.username}'
                SendMessage(paid_group_id, text).post()
                return 'Запит надіслано'
            else:
                print('user not found')
                error = 'Користувача не знайдено'
                return redirect(url_for('main.error'), error)
        else:
            print('request not found')
            error = 'Запит не знайдено'
            return redirect(url_for('main.error'), error)
    else:
        print('specialist not found')
        error = 'Спеціаліста не знідено'
        return redirect(url_for('main.error'), error)


@bp.route('/form/update_selected_tags', methods=['POST'])
def update_selected_tags():
    form = NewSpecialistForm(request.form)
    tags = form.tags
    if tags:
        print('/n/n-----------/n')
        print('form tags: ', tags)
        form = NewSpecialistForm(

        )
