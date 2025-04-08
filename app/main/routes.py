from flask import render_template
from app.main import bp


@bp.get("/")
def index():
    return render_template("index.html")

