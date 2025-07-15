# Handles database operations

# Python Libraries
from sqlite3 import connect, Connection
from os import path


# Helper function to convert images to binary
def image_to_blob(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        blob: bytes = image_file.read()
    return blob


# Get absolute path to resource; necessary for compilation.
def absolute_path(file_name: str) -> str:
    return path.abspath(path.join(path.dirname(__file__), file_name))


class PokedexDB:
    def __init__(self):
        self.database: str = absolute_path("db.sqlite3")

    def _connect(self) -> Connection:
        return connect(self.database)

    # Get dict of Pokémon header data (type_set_id, stat_set_id, etc.) for passed game and dex names.
    def get_pokedex_headers(self, game: str, dex: str) -> dict:
        query: str = """
            SELECT pokedex.pokemon_id
                ,pokedex.type_set_id
                ,pokedex.stat_set_id
                ,pokedex.ability_set_id
                ,game.id AS [game_id]
            FROM pokedex
            JOIN game_pokedex ON game_pokedex.id = pokedex.game_pokedex_id
            JOIN game ON game.id = game_pokedex.game_id
            WHERE game.name = ?
                AND game_pokedex.name = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex))
        return {pd[0]: list(pd[1:]) for pd in cursor.fetchall()}

    # Return a list of Pokémon base forms from the National Dex
    def get_pokemon(self, game: str, dex: str) -> list:
        query: str = """
            SELECT pokemon.national_pokedex_id
                ,pokedex.pokedex_order
                ,pokemon.name
            FROM pokemon
            JOIN pokedex ON pokedex.pokemon_id = pokemon.id
            JOIN game_pokedex ON game_pokedex.id = pokedex.game_pokedex_id
            JOIN game ON game.id = game_pokedex.game_id
            WHERE pokemon.form_id = 1 AND game.name = ?
                AND game_pokedex.name = ?
            ORDER BY pokedex.pokedex_order
                ,pokemon.form_id
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex))
            return cursor.fetchall()

    # Return a list of Pokémon base forms from the National Dex
    def get_forms(self, game: str, dex: str, national_dex_id: int) -> list:
        query: str = """
            SELECT pokemon.id
                ,pokemon.form_name
            FROM pokemon
            JOIN pokedex ON pokedex.pokemon_id = pokemon.id
            JOIN game_pokedex ON game_pokedex.id = pokedex.game_pokedex_id
            JOIN game ON game.id = game_pokedex.game_id
            WHERE game.name = ?
                AND game_pokedex.name = ?
                AND pokemon.national_pokedex_id = ?
            ORDER BY pokemon.form_id
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex, national_dex_id))
            return cursor.fetchall()

    # Get byte data for a Pokémon's types.
    def get_type_icons(self, type_set_id: int) -> tuple:
        query: str = """
            SELECT type1.icon AS [type1_icon]
                ,type2.icon AS [type2_icon]
            FROM type_set
            JOIN type AS [type1] ON type1.id = type_set.primary_type_id
            JOIN type AS [type2] ON type2.id = type_set.secondary_type_id
            WHERE type_set.id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (type_set_id,))
            return cursor.fetchone()

    # Return a list of Pokémon stats
    def get_stats(self, stat_set_id: int) -> list:
        query: str = """
            SELECT hp
                ,atk
                ,def
                ,spa
                ,spd
                ,spe
            FROM stat_set
            WHERE id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (stat_set_id,))
            return list(cursor.fetchone())

    # Return a tuple of max Pokémon stats (max HP, max other stats)
    def get_max_stats(self, game_id: int) -> tuple:
        query: str = """
            SELECT MAX(stat_set.HP) AS [max_hp_stat]
                ,MAX(MAX(stat_set.ATK, stat_set.DEF, stat_set.SPA, stat_set.SPE)) [max_non_hp_stat]
            FROM pokedex
            JOIN game_pokedex ON game_pokedex.id = pokedex.game_pokedex_id
            JOIN stat_set ON stat_set.id = pokedex.stat_set_id
            WHERE game_pokedex.game_id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game_id,))
            max_stats = cursor.fetchone()
            return max_stats if max_stats != (None, None) else (0, 0)

    # Return tuple of ability names for passed ability set ID.
    def get_abilities(self, ability_set_id: int) -> tuple:
        query: str = """
            SELECT IFNULL(primary_ability.name, 'N/A') AS [primary_ability_name]
                ,IFNULL(secondary_ability.name, 'N/A') AS [secondary_ability_name]
                ,IFNULL(hidden_ability.name, 'N/A') AS [hidden_ability_name]
            FROM ability_set
            JOIN ability AS [primary_ability] ON primary_ability.id = ability_set.primary_ability_id
            JOIN ability AS [secondary_ability] ON secondary_ability.id = ability_set.secondary_ability_id
            JOIN ability AS [hidden_ability] ON hidden_ability.id = ability_set.hidden_ability_id
            WHERE ability_set.id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ability_set_id,))
            return cursor.fetchone()

    # Return a list of all games in the database.
    def get_games(self) -> list:
        query: str = """
            SELECT game.name
            FROM game
            ORDER BY game.id
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [game[0] for game in cursor.fetchall()]

    # Return a list of Pokedex names for a specific game.
    def get_pokedexes(self, game_name: str) -> list:
        query: str = """
            SELECT game_pokedex.name AS [game_pokedex_name]
            FROM game_pokedex
            JOIN game ON game.id = game_pokedex.game_id
            WHERE game.name = ?
            ORDER BY game_pokedex.id
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game_name,))
            return [dex[0] for dex in cursor.fetchall()]

    # Get byte data for a Pokémon's appearance
    def get_portrait_icon(self, pokemon_id: int, is_shiny: bool) -> bytes:
        icon: str = "icon_shiny" if is_shiny else "icon_normal"
        query: str = f"""
            SELECT pokemon.{icon}
            FROM pokemon
            WHERE pokemon.id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (pokemon_id,))
            return cursor.fetchone()[0]

    # Update byte data for a Pokémon's normal appearance
    def update_portrait_icon(self, image_blob: bytes, pokemon_id: int, is_shiny: bool) -> None:
        icon: str = "icon_shiny" if is_shiny else "icon_normal"
        query: str = f"""
            UPDATE pokemon
            SET pokemon.{icon} = ?
            WHERE pokemon.id = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (image_blob, pokemon_id))
            conn.commit()

# Update byte data for a Pokémon's normal appearance
#def update_type_icon():
#    path = "C:/Users/NathanJones/Downloads"
#    for file in os.listdir(path):
#        if file.endswith(".png"):
#            blob = image_to_blob(f"{path}/{file}")
#            type_id = int(file.split(".")[0])
#            conn = sqlite3.connect(f"{dirname(__file__)}/PokeDB.sqlite3")
#            cursor = conn.cursor()
#            cursor.execute(f"""
#                update Type
#                set TypeIcon = ?
#                where TypeID = ?
#                """, (blob, type_id))
#            conn.commit()
#            conn.close()
# update_type_icon()
