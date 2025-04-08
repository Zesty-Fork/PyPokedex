import json

from flask import request, jsonify, Response
from app.api import bp
from app.models.api import Game, GamePokedex


@bp.get("/")
def index():
    return json.dumps({"Here": "We Are"})


@bp.get("/games")
def get_games():
    status_code: int = 200
    games: list = Game.query.all()
    return jsonify([game.serialized for game in games]), status_code


@bp.get("/games/<game_id>")
def get_game(game_id: int):
    status_code: int = 200
    game: Game = Game.query.filter(Game.id == game_id).first()
    if game:
        response: Response = jsonify(game.serialized)
    else:
        response: Response = jsonify({"error": "The game with the specified ID does not exist. (404)"})
        status_code = 404
    return response, status_code


@bp.get("/games/<game_id>/pokedexes")
def get_game_pokedexes(game_id: int):
    status_code: int = 200
    game_pokedexes: GamePokedex = GamePokedex.query.filter(GamePokedex.game_id == game_id).all()
    return jsonify([game_pokedex.serialized for game_pokedex in game_pokedexes]), status_code
