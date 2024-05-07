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