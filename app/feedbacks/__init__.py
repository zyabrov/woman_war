from flask import Blueprint

bp = Blueprint('feedbacks', __name__, url_prefix='/feedbacks', template_folder='templates')

from app.requests import routes