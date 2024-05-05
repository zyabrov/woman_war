from flask import Blueprint

bp = Blueprint('specialists', __name__, url_prefix='/specialists')

from app.specialists import routes