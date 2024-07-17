from app.feedbacks import bp
from app.feedbacks.models import Feedback
from flask import render_template, redirect, url_for, request


@bp.route('/', methods=['GET', 'POST'])
def feedbacks():
    return "feedbacks"


@bp.route('/<int:feedback_id>', methods=['GET', 'POST'])
def feedback_card(feedback_id):
    feedback = Feedback.get(feedback_id)
    return render_template('feedback_card.html', feedback=feedback)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    from app.manychat.models import ManychatRequest
    request_data = request.get_json()
    print('/n/n----------------/n')
    print('request_data: ', request_data)
    manychat_request = ManychatRequest(request_data)
    from app.requests.models import Request
    r = Request.get(manychat_request.id)
    questions = []
    for i in range(1, 11):
        questions.append(request_data['custom_fields'].get('Відгук - питання ' + str(i)))    
    feedback = Feedback.add_from_request(r, questions)
    r.status = 'Відгук отримано'
    r.save()
    return {'status': '200', 'feedback_id': feedback.id, 'feedback_data': feedback.to_dict(), 'request_id': r.id}
