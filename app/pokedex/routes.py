from flask import render_template
from app.pokedex import bp


@bp.get("/")
def index():
    return render_template("pokedex/index.html")


@bp.get("/editor/")
def editor():
    return render_template("pokedex/editor.html")
