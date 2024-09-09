import sqlite3


class PokeDexDB:
    def __init__(self):
        self._database: str = "DB/PokeDB.sqlite3"

    # Return a list of Pokémon base forms from the National Dex
    def get_national_dex_pokemon(self) -> list:
        national_dex_pokemon: list = []
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select PokemonID
                    ,NationalDexID
                    ,PokemonName || ' [' || FormName || ']' as PokemonName
                from NationalDex
                order by NationalDexID, FormID
                """)
            national_dex_pokemon.extend(cursor.fetchall())
        return national_dex_pokemon

    # Get byte data for a Pokémon's normal appearance
    def get_icon_normal(self, pokemon_id: int) -> bytes:
        img_data: bytes = bytes(0)
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select IconNormal
                from NationalDex
                where PokemonID = ?
                """, (pokemon_id,))
            if cursor.rowcount:
                img_data = cursor.fetchone()[0]
        return img_data

    # Get byte data for a Pokémon's shiny appearance
    def get_icon_shiny(self, pokemon_id: int) -> bytes:
        img_data: bytes = bytes(0)
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select IconShiny
                from NationalDex
                where PokemonID = ?
                """, (pokemon_id,))
            if cursor.rowcount:
                img_data = cursor.fetchone()[0]
        return img_data

    # Update byte data for a Pokémon's normal appearance
    def update_icon_normal(self, pokemon_id: int, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update NationalDex
                set IconNormal = ?
                where PokemonID = ?
                """, (image_blob, pokemon_id))
            conn.commit()

    # Update byte data for a Pokémon's shiny appearance
    def update_icon_shiny(self, pokemon_id: int, image_blob: bytes):
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                update NationalDex
                set IconShiny = ?
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
