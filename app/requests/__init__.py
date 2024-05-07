from flask import Blueprint

bp = Blueprint('requests', __name__, url_prefix='/requests', template_folder='templates')

from app.requests import routes