from flask import Blueprint

bp = Blueprint('manychat', __name__, url_prefix='/manychat')

from app.manychat import routes