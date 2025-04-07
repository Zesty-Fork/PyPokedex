from flask import render_template
from app.pokedex import bp
from app.models.pokedex import Pokemon, Game, GamePokedex


@bp.route("/")
def index():
    games: list = Game.query.all()
    game_pokedexes: list = GamePokedex.query.all()
    pokemon: list = Pokemon.query.all()
    return render_template("pokedex/index.html", games=games, game_pokedexes=game_pokedexes, pokemon_data=pokemon)


@bp.route("/editor/")
def editor():
    return render_template("pokedex/editor.html")
