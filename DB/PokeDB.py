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
        self.cur_pokemon_id: int = 0
        self.cur_game: str = ""
        self.cur_dex: str = ""

    # Return a list of Pokémon base forms from the National Dex
    def get_pokemon(self) -> list:
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
            """, (self.cur_game, self.cur_dex))
        pokemon: list = [p for p in cursor.fetchall()]
        conn.close()
        return pokemon

    # Return a list of Pokémon stats
    def get_stats(self) -> list:
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
            """, (self.cur_pokemon_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            pkmn_stats.extend(result)
        else:
            pkmn_stats.extend([0, 0, 0, 0, 0, 0])
        return pkmn_stats

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

    def get_dexes(self) -> list:
        print(self.cur_dex)
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
            select gd.GameDexName
            from GameDex gd
            join Game g on g.GameID = gd.GameID
            where g.GameName = ?
            order by gd.GameDexID
            """, (self.cur_game, ))
        dexes: list = [dex[0] for dex in cursor.fetchall()]
        conn.close()
        return dexes

    # Get byte data for a Pokémon's appearance
    def get_pkmn_icon(self, shiny: bool) -> bytes:
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
            """, (self.cur_pokemon_id,))
        img_data: bytes = cursor.fetchone()[0]
        conn.close()
        return img_data

    # Update byte data for a Pokémon's normal appearance
    def update_icon_normal(self, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update Pokemon
                set IconNormal = ?
                where PokemonID = ?
                """, (image_blob, self.cur_pokemon_id))
            conn.commit()

    # Update byte data for a Pokémon's shiny appearance
    def update_icon_shiny(self, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update NationalDex
                set IconShiny = ?
                where PokemonID = ?
                """, (image_blob, self.cur_pokemon_id))
            conn.commit()

    def split_gender_forms(self):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("update NationalDex set FormName = 'Male' where PokemonID = ?", (self.cur_pokemon_id,))
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
                """, (self.cur_pokemon_id,))
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
                """, (self.cur_pokemon_id,))
            conn.commit()

    def add_gigantamax_form(self):
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
                """, (self.cur_pokemon_id,))
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
                """, (self.cur_pokemon_id,))
            conn.commit()

    def set_pokemon_id(self, pokemon_id: int) -> None:
        self.cur_pokemon_id = pokemon_id
        if not self.cur_pokemon_id:
            self.cur_pokemon_id = 0
