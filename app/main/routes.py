from flask import render_template, request, Blueprint

from app.main import bp
from app.extensions import db


@bp.route('/create_tables', methods=['GET', 'POST'])
def create_tables():
    db.drop_all()
    db.create_all()
    return 'tables_created'