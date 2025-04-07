from flask import Blueprint

bp = Blueprint("pokedex", __name__)

from app.pokedex import routes
