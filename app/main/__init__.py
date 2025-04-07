from flask import Blueprint

bp: Blueprint = Blueprint("main", __name__)

from app.main import routes
