from app.feedbacks import bp
from app.feedbacks.models import Feedback
from flask import render_template, redirect, url_for, request


@bp.route('/new', methods=['GET', 'POST'])
def new():
    from app.manychat.models import ManychatRequest
    request_data = request.get_json()
    print('/n/n----------------/n')
    print('request_data: ', request_data)
    manychat_request = ManychatRequest(request_data)
    r = Request.get(manychat_request.id)
    from app.requests.models import Request
    questions = []
    for i in range(1, 11):
        questions.append(request_data['custom_fields'].get('Відгук - питання ' + str(i)))    
    feedback = Feedback.add_from_request(r, questions)
    return {'status': '200', 'feedback_id': feedback.id}
