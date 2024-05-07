from flask import render_template, Blueprint, request
from app.users import bp
from app.extensions import db
from app.users.models import User


@bp.route('/')
def users():
    return render_template('users.html')


@bp.route('/new', methods=['GET', 'POST'])
def new_user():
    print('request.data', request.data)
    user = User.add_user(request.data)
    if user:
        return 'user_created: {}'.format(user)
    return 'user_not_created'

@bp.route('/new_user_test', methods=['GET', 'POST'])
def new_user_test():
    user = User.add_user()
    if user:
        return 'user_created: {}'.format(user)
    return 'user_not_created'


@bp.route('/<int:user_id>', methods=['GET', 'POST'])
def user_card(user_id):
    user = User.get(user_id)
    if user:
        return render_template('user_card.html', user=user)