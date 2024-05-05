from flask import render_template, Blueprint, request
from app.tags import bp
from app.tags.models import Tag