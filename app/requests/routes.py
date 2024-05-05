from flask import render_template, Blueprint, request
from app.requests import bp
from app.requests.models import Request

server_url = 'http://127.0.0.1:5000'

@bp.route("/requests", methods=["GET", "POST"])
def requests():
    return render_template("requests/requests.html")
    