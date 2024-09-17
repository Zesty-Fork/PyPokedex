"""
SELECT max(ss.HP) as  MaxHP
	,max(max(ss.ATK, ss.DEF, ss.SPA, ss.SPE)) as  MaxStat
FROM Pokemon as p
JOIN PokeDex as pd on pd.PokemonID = p.PokemonID
JOIN GameDex as gd on gd.GameDexID = pd.GameDexID
JOIN StatSet as ss on ss.StatSetID = pd.StatSetID
WHERE gd.GameDexID = 25
"""

# Handles database operations

# Python Libraries
import sqlite3


class PokeDexDB:
    def __init__(self):
        self._database: str = "DB/PokeDB.sqlite3"

    # Return a list of Pokémon base forms from the National Dex
    def get_pkmn_national_dex(self) -> list:
        national_dex_pokemon: list = []
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select PokemonID
                    ,NationalDexID
                    ,PokemonName
                from Pokemon
                where FormID = 1
                order by NationalDexID, FormID
                """)
            national_dex_pokemon.extend(cursor.fetchall())
        return national_dex_pokemon

    # Return a list of Pokémon stats
    def get_pkmn_stats(self, pkmn_id: int) -> list:
        pkmn_stats: list = []
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select HP
                ,ATK
                ,DEF
                ,SPA
                ,SPD
                ,SPE
            from StatSet s
            join PokeDex pd on pd.StatSetID = s.StatSetID
            where pd.PokemonID = ?
            """, (pkmn_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            pkmn_stats.extend(result)
        else:
            pkmn_stats.extend([0, 0, 0, 0, 0, 0])
        return pkmn_stats

    def get_games(self):
        games: dict = {}
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select GameID
                ,GameName
            from Game
            order by GameID
            """)
        for game_id, game_name in cursor.fetchall():
            games[game_name] = game_id
        conn.close()
        return games

    # Get byte data for a Pokémon's appearance
    def get_pkmn_icon(self, pkmn_id: int, shiny: bool) -> bytes:
        icon: str = ""
        if shiny:
            icon += "IconShiny"
        else:
            icon += "IconNormal"
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute(f"""
            select {icon}
            from Pokemon
            where PokemonID = ?
            """, (pkmn_id,))
        img_data: bytes = cursor.fetchone()[0]
        conn.close()
        return img_data

    # Update byte data for a Pokémon's normal appearance
    def update_icon_normal(self, pkmn_id: int, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update Pokemon
                set IconNormal = ?
                where PokemonID = ?
                """, (image_blob, pkmn_id))
            conn.commit()

    # Update byte data for a Pokémon's shiny appearance
    def update_icon_shiny(self, pkmn_id: int, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update NationalDex
                set IconShiny = ?
                where PokemonID = ?
                """, (image_blob, pkmn_id))
            conn.commit()

    def split_gender_forms(self, pkmn_id: int):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("update NationalDex set FormName = 'Male' where PokemonID = ?", (pkmn_id,))
            cursor.execute("""
                insert into NationalDex (NationalDexID, FormID, PokemonName, FormName)
                select nd.NationalDexID
                    ,ndf.MaxFormID + 1 as NextFormID
                    ,nd.PokemonName
                    ,'Female' as FormName
                from NationalDex nd
                join (
                    select NationalDexID
                        ,Max(FormID) as MaxFormID
                    from NationalDex
                    group by NationalDexID
                    ) ndf on ndf.NationalDexID = nd.NationalDexID
                where nd.PokemonID = ?
                """, (pkmn_id,))
            cursor.execute("""
                insert into PokemonStats (PokemonID, GenerationID, HP, ATK, DEF, SPA, SPD, SPE)
                select (select Max(PokemonID) from NationalDex)
                    ,GenerationID
                    ,HP
                    ,ATK
                    ,DEF
                    ,SPA
                    ,SPD
                    ,SPE
                from PokemonStats
                where PokemonID = ?
                """, (pkmn_id,))
            conn.commit()

    def add_gigantamax_form(self, pkmn_id: int):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into NationalDex (NationalDexID, FormID, PokemonName, FormName)
                select nd.NationalDexID
                    ,ndf.MaxFormID + 1 as NextFormID
                    ,nd.PokemonName
                    ,'Gigantamax' as FormName
                from NationalDex nd
                join (
                    select NationalDexID
                        ,Max(FormID) as MaxFormID
                    from NationalDex
                    group by NationalDexID
                    ) ndf on ndf.NationalDexID = nd.NationalDexID
                where nd.PokemonID = ?
                """, (pkmn_id,))
            cursor.execute("""
                insert into PokemonStats (PokemonID, GenerationID, HP, ATK, DEF, SPA, SPD, SPE)
                select (select Max(PokemonID) from NationalDex)
                    ,GenerationID
                    ,HP
                    ,ATK
                    ,DEF
                    ,SPA
                    ,SPD
                    ,SPE
                from PokemonStats
                where PokemonID = ?
                    and GenerationID = 8
                """, (pkmn_id,))
            conn.commit()
