from flask import Blueprint

bp = Blueprint('requests', __name__, url_prefix='/requests')

from app.requests import routes