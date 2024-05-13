from flask import Blueprint

bp = Blueprint('telegram', __name__, url_prefix='/telegram', template_folder='templates')

from app.telegram import routes