# Handles database operations

# Python Libraries
from sqlite3 import connect, Connection


# Helper function to convert images to binary
def image_to_blob(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        blob: bytes = image_file.read()
    return blob


class PokedexDB:
    def __init__(self):
        self.database: str = "db/db.sqlite3"

    def _connect(self) -> Connection:
        return connect(self.database)

    # Get dict of Pokémon header data (TypeSetID, StatSetID, etc.) for passed game and dex names.
    def get_pokedex_headers(self, game: str, dex: str) -> dict:
        query: str = """
            SELECT pd.PokemonID, pd.TypeSetID, pd.StatSetID, pd.AbilitySetID, g.GameID
            FROM PokeDex pd
            JOIN GameDex gd ON gd.GameDexID = pd.GameDexID
            JOIN Game g ON g.GameID = gd.GameID
            WHERE g.GameName = ? AND gd.GameDexName = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex))
        return {pd[0]: list(pd[1:]) for pd in cursor.fetchall()}

    # Return a list of Pokémon base forms from the National Dex
    def get_pokemon(self, game: str, dex: str) -> list:
        query: str = """
            SELECT p.NationalDexID, pd.DexOrder, p.PokemonName
            FROM Pokemon p
            JOIN PokeDex pd ON pd.PokemonID = p.PokemonID
            JOIN GameDex gd ON gd.GameDexID = pd.GameDexID
            JOIN Game g ON g.GameID = gd.GameID
            WHERE p.FormID = 1 AND g.GameName = ? AND gd.GameDexName = ?
            ORDER BY pd.DexOrder, p.FormID
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex))
            return cursor.fetchall()

    # Return a list of Pokémon base forms from the National Dex
    def get_forms(self, game: str, dex: str, national_dex_id: int) -> list:
        query: str = """
            SELECT p.PokemonID, p.FormName
            FROM Pokemon p
            JOIN PokeDex pd ON pd.PokemonID = p.PokemonID
            JOIN GameDex gd ON gd.GameDexID = pd.GameDexID
            JOIN Game g ON g.GameID = gd.GameID
            WHERE g.GameName = ? AND gd.GameDexName = ? AND p.NationalDexID = ?
            ORDER BY p.FormID
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game, dex, national_dex_id))
            return cursor.fetchall()

    # Get byte data for a Pokémon's types.
    def get_type_icons(self, type_set_id: int) -> tuple:
        query: str = """
            SELECT t1.TypeIcon, t2.TypeIcon
            FROM TypeSet ts
            JOIN Type t1 ON t1.TypeID = ts.PrimaryTypeID
            JOIN Type t2 ON t2.TypeID = ts.SecondaryTypeID
            WHERE ts.TypeSetID = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (type_set_id,))
            return cursor.fetchone()

    # Return a list of Pokémon stats
    def get_stats(self, stat_set_id: int) -> list:
        query: str = """
            SELECT HP, ATK, DEF, SPA, SPD, SPE
            FROM StatSet
            WHERE StatSetID = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (stat_set_id,))
            return list(cursor.fetchone())

    # Return a tuple of max Pokémon stats (max HP, max other stats)
    def get_max_stats(self, game_id: int) -> tuple:
        query: str = """
            SELECT MAX(ss.HP), MAX(MAX(ss.ATK, ss.DEF, ss.SPA, ss.SPE))
            FROM PokeDex pd
            JOIN GameDex gd ON gd.GameDexID = pd.GameDexID
            JOIN StatSet ss ON ss.StatSetID = pd.StatSetID
            WHERE gd.GameID = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game_id,))
            max_stats = cursor.fetchone()
            return max_stats if max_stats != (None, None) else (0, 0)

    # Return tuple of ability names for passed ability set ID.
    def get_abilities(self, ability_set_id: int) -> tuple:
        query: str = """
            SELECT IFNULL(a1.AbilityName, 'N/A'), IFNULL(a2.AbilityName, 'N/A'), IFNULL(a3.AbilityName, 'N/A')
            FROM AbilitySet abs
            JOIN Ability a1 ON a1.AbilityID = abs.PrimaryAbilityID
            JOIN Ability a2 ON a2.AbilityID = abs.SecondaryAbilityID
            JOIN Ability a3 ON a3.AbilityID = abs.HiddenAbilityID
            WHERE abs.AbilitySetID = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ability_set_id,))
            return cursor.fetchone()

    # Return a list of all games in the database.
    def get_games(self) -> list:
        query: str = """
            SELECT GameName
            FROM Game
            ORDER BY GameID
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [game[0] for game in cursor.fetchall()]

    # Return a list of Pokedex names for a specific game.
    def get_dexes(self, game: str) -> list:
        query: str = """
            SELECT gd.GameDexName
            FROM GameDex gd
            JOIN Game g ON g.GameID = gd.GameID
            WHERE g.GameName = ?
            ORDER BY gd.GameDexID
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (game,))
            return [dex[0] for dex in cursor.fetchall()]

    # Get byte data for a Pokémon's appearance
    def get_portrait_icon(self, pokemon_id: int, shiny: bool) -> bytes:
        icon: str = "IconShiny" if shiny else "IconNormal"
        query: str = f"""
            SELECT {icon}
            FROM Pokemon
            WHERE PokemonID = ?
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (pokemon_id,))
            return cursor.fetchone()[0]

    # Update byte data for a Pokémon's normal appearance
    def update_portrait_icon(self, image_blob: bytes, pokemon_id: int, shiny: bool) -> None:
        icon: str = "IconShiny" if shiny else "IconNormal"
        query: str = f"""
            UPDATE Pokemon
            SET {icon} = ?
            WHERE PokemonID = ?
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
