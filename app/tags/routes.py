from flask import render_template, Blueprint, request
from app.tags import bp
from app.tags.models import Tag


@bp.route('/new_tag', methods=['GET', 'POST'])
def new():
    pass


@bp.route('/new_tag/<string:name>', methods=['GET', 'POST'])
def new_tag(name):
    tag = Tag.get_by_name(name)
    if not tag:
        tag = Tag.add(name)
        if tag:
            return render_template('tags.html', tags=Tag.query.all())
        else:
            return 'The Tag was not added'
    return 'The Tag already exists'


@bp.route('/', methods=['GET', 'POST'])
def tags():
    return render_template('tags.html', tags=Tag.query.all())
