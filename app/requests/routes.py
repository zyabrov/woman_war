from app.requests import bp
from app.requests.models import Request
from flask import render_template, redirect, url_for, request, send_file
import xlsxwriter

@bp.route('/')
def requests():
    requests = Request.query.order_by(Request.id.desc()).all()
    return render_template('requests.html', requests=requests)

@bp.route('/free', methods=['POST'])
def free_request():
    from app.manychat.models import ManychatRequest
    from app.users.models import User
    manychat_request = ManychatRequest(request.get_json())
    user = User.get_and_update_or_create_from_request(manychat_request)
    print('\n\n----------------\n')
    print('free request user: ', user)
    r = Request.add(manychat_request)
    if r:
        print('new free request: ', r)
        r.save_message_id(manychat_request.message_id)
        return {'status': '200', 'id': r.id}
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
    if specialist:
        print('\n\n----------------\n')
        print('user request id: ', manychat_request.user_request_id)
        print('specialist: ', specialist)
        r = Request.get(int(manychat_request.user_request_id))
        if r:
            print('request:', r)
            r.add_specialist(specialist.id)

            #edit the group message
            message_id = int(r.message_id)
            message_text = f'Запит {r.id} прийняв спеціаліст @{specialist.telegram_username}'
            UpdateMessage(free_group_id, message_id, message_text).post()

            #message to the user
            user_message = TextMessage(f'Ваш запит прийняв спеціаліст: {specialist.name} @{specialist.telegram_username}')
            ManychatSendMessage(r.user_id, messages=[user_message.json]).post()

            #message to the specialist
            specialist_message = TextMessage(
                f'''Запит {r.id} від {r.user_full_name} (@{r.user_username}) прийнятий. 

                Запит:{r.request_name}
                Вік: {r.user_age}
                _____
                Телефон: {r.user_phone}
                ''')
            ManychatSendMessage(specialist.id, messages=[specialist_message.json]).post()

        else:
            print('request not found')
    else:
        print('specialist not found')

        
    return {'status': '200'}


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
                return {'status': '404', 'specialists': 0, 'message': message}
            
        else:
            print('/n/n----------------/n')
            print('no request found')
            message = 'Запит не знайдено'
            return {'status': '404', 'specialists': 0, 'message': message}

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
            r.status = 'Запит відгуку відправлено'
            r.save()
            return '✅'

    return {'status': '404'}
           

@bp.route('/generate_xls', methods=['GET', 'POST'])
def generate_xls():
    table_data = []  # Example table data

    # Add data to the table
    for r in Request.query.all():
        row_data = {
            'ID': r.id,
            'Запит': r.request_name,
            'Коли створений': r.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Клієнт': r.user_full_name,
            'Cпеціаліст': r.specialist.name if r.specialist else '',
            'Вік': r.user_age,
            'Де знаходиться': r.user_where_is,
            'Місто': r.user_where_is_city,
            'Досвід з психологом': r.user_worked_with_psychologist_before,
            'Яку допомогу': r.help_type,
            'Як дізналися': r.user_how_known,
            'Телефон': r.user_phone,
            'Тип запиту': r.request_type
        }    
        table_data.append(row_data)

    # Generate XLS file using the table data
    workbook = xlsxwriter.Workbook('app/static/requests.xlsx')
    worksheet = workbook.add_worksheet()

     # Write the data from table_data to the Excel file
    for row_idx, row in enumerate(table_data):
        for col_idx, value in enumerate(row.values()):
            worksheet.write(row_idx, col_idx, value)

    workbook.close()

    # Send the XLS file back to the client for download
    return send_file('static/requests.xlsx', as_attachment=True, download_name='requests.xlsx')

