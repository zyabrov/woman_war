from flask import Blueprint

bp = Blueprint('tags', __name__, url_prefix='/tags', template_folder='templates')

from app.tags import routes