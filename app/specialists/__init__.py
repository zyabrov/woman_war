from flask import Blueprint

bp = Blueprint('specialists', __name__, url_prefix='/specialists', template_folder='templates')

from app.specialists import routes