from flask import render_template, Blueprint, request
from app.specialists import bp
from app.specialists.models import Specialist


@bp.route('/', methods=['GET', 'POST'])
def specialists():
    return render_template('specialists/index.html')


@bp.route('/<int:specialist_id>', methods=['GET', 'POST'])
def specialist(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if specialist:
        
        if request:
            request.add_specialist(specialist)
            return request.specialist_card_response(specialist)