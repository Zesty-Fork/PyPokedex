"""
SELECT max(ss.HP) as  MaxHP
,max(max(ss.ATK, ss.DEF, ss.SPA, ss.SPE)) as  MaxStat
FROM Pokemon as p
JOIN PokeDex as pd on pd.PokemonID = p.PokemonID
JOIN GameDex as gd on gd.GameDexID = pd.GameDexID
JOIN StatSet as ss on ss.StatSetID = pd.StatSetID
WHERE gd.GameDexID = 25
"""
import os
# Handles database operations

# Python Libraries
import sqlite3
from os.path import dirname


# Helper function to convert images to binary
def image_to_blob(image_path: str) -> bytes:
    blob: bytes = b""
    with open(image_path, "rb") as image_file:
        blob = image_file.read()
    return blob


class PokeDexDB:
    def __init__(self):
        self._database: str = f"{dirname(__file__)}/PokeDB.sqlite3"

    def get_pokedex_headers(self, game: str, dex: str) -> dict:
        pokedex_headers: dict = {}
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select pd.PokemonID
                ,pd.TypeSetID
                ,pd.StatSetID
                ,pd.AbilitySetID
            from PokeDex pd
            join GameDex gd on gd.GameDexID = pd.GameDexID
            join Game g on g.GameID = gd.GameID
            where g.GameName = ?
                and gd.GameDexName = ?
            """, (game, dex))
        for pd in cursor.fetchall():
            pokedex_headers[pd[0]] = list(pd[1:])
        conn.close()
        return pokedex_headers

    # Return a list of Pokémon base forms from the National Dex
    def get_pokemon(self, game: str, dex: str) -> list:
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select p.PokemonID
                ,pd.DexOrder
                ,p.PokemonName
            from Pokemon p
            join PokeDex pd on pd.PokemonID = p.PokemonID
            join GameDex gd on gd.GameDexID = pd.GameDexID
            join Game g on g.GameID = gd.GameID
            where p.FormID = 1
                and g.GameName = ?
                and gd.GameDexName = ?
            order by pd.DexOrder, p.FormID
            """, (game, dex))
        pokemon: list = [p for p in cursor.fetchall()]
        conn.close()
        return pokemon

    # Get byte data for a Pokémon's types.
    def get_type_icons(self, type_set_id: int) -> tuple:
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select t1.TypeIcon as TypeIcon1
                ,t2.TypeIcon as TypeIcon2
            from TypeSet ts
            join Type t1 on t1.TypeID = ts.PrimaryTypeID
            join Type t2 on t2.TypeID = ts.SecondaryTypeID
            where ts.TypeSetID = ?
            """, (type_set_id,))
        type_icons: tuple = cursor.fetchone()
        conn.close()
        return type_icons

    # Return a list of Pokémon stats
    def get_stats(self, stat_set_id: int) -> list:
        stats: list = []
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select HP
                ,ATK
                ,DEF
                ,SPA
                ,SPD
                ,SPE
            from StatSet
            where StatSetID = ?
            """, (stat_set_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stats.extend(result)
        else:
            stats.extend([0, 0, 0, 0, 0, 0])
        return stats

    def get_games(self) -> list:
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select GameName
            from Game
            order by GameID
            """)
        games: list = [game[0] for game in cursor.fetchall()]
        conn.close()
        return games

    def get_dexes(self, game: str) -> list:
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select gd.GameDexName
            from GameDex gd
            join Game g on g.GameID = gd.GameID
            where g.GameName = ?
            order by gd.GameDexID
            """, (game,))
        dexes: list = [dex[0] for dex in cursor.fetchall()]
        conn.close()
        return dexes

    # Get byte data for a Pokémon's appearance
    def get_pkmn_icon(self, pokemon_id: int, shiny: bool) -> bytes:
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
            """, (pokemon_id,))
        img_data: bytes = cursor.fetchone()[0]
        conn.close()
        return img_data

    # Update byte data for a Pokémon's normal appearance
    def update_pkmn_icon(self, image_blob: bytes, pokemon_id: int, shiny: bool):
        icon: str = ""
        if shiny:
            icon += "IconShiny"
        else:
            icon += "IconNormal"
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                update Pokemon
                set {icon} = ?
                where PokemonID = ?
                """, (image_blob, pokemon_id))
            conn.commit()

    def split_gender_forms(self, pokemon_id: int):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("update NationalDex set FormName = 'Male' where PokemonID = ?", (pokemon_id,))
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
                """, (pokemon_id,))
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
                """, (pokemon_id,))
            conn.commit()

    def add_gigantamax_form(self, pokemon_id: int):
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
                """, (pokemon_id,))
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
                """, (pokemon_id,))
            conn.commit()


# Update byte data for a Pokémon's normal appearance
def update_type_icon():
    path = "C:/Users/NathanJones/Downloads"
    for file in os.listdir(path):
        if file.endswith(".png"):
            blob = image_to_blob(f"{path}/{file}")
            type_id = int(file.split(".")[0])
            conn = sqlite3.connect(f"{dirname(__file__)}/PokeDB.sqlite3")
            cursor = conn.cursor()
            cursor.execute(f"""
                update Type
                set TypeIcon = ?
                where TypeID = ?
                """, (blob, type_id))
            conn.commit()
            conn.close()
update_type_icon()