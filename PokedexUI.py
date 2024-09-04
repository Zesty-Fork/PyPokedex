# Python Libraries
import tkinter as tk
from tkinter import ttk
import sqlite3

# Global Declarations
TITLE: str = "RegionalDexBuilder"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind
IMAGE: str = r"C:\Users\NathanJones\Desktop\Projects\_complete\Recycle Bin - Shortcut\PokeGit\PyPokedex\Pokémon HOME\Pokémon Icons\poke_icon_0001_000_mf_n_00000000_f_n.png"
PKMN_ID: int = 0


def image_to_blob(image_path: str) -> bytes:
    blob: bytes = b""
    with open(image_path, "rb") as image_file:
        blob = image_file.read()
    return blob


class RegionalDexBuilder:
    def __init__(self, pokedex_db: str):
        self.pokedex_db: str = pokedex_db

    def get_db_conn(self):
        return sqlite3.connect(self.pokedex_db)

    def create_main_window(self):
        root = tk.Tk()
        root.title(TITLE)
        root.geometry("800x600")
        root.resizable(False, False)

        # Windows OS only (remove the minimize/maximize button)
        try:
            root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")

        columns = ["NationalDexNo", "PokemonName"]
        self.pkmn_tree = ttk.Treeview(root, columns=columns, show='headings')
        self.pkmn_tree.column("NationalDexNo", width=30, minwidth=30)
        self.pkmn_tree.bind("<<TreeviewSelect>>", self._pokemon_selected)

        # Define headings
        self.pkmn_tree.heading("NationalDexNo", text="#")
        self.pkmn_tree.heading("PokemonName", text="Pokemon")

        icon = tk.PhotoImage(data=db_get_icon())  # Replace with your icon
        image_label = tk.Label(root, image=icon)

        self.pkmn_tree.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        image_label.pack(side=tk.LEFT)
        for pokemon in self.get_national_dex_pokemon():
            self.pkmn_tree.insert("", tk.END, values=pokemon)
        # layout on the root window
        root.mainloop()

    def get_national_dex_pokemon(self) -> list:
        conn = self.get_db_conn()
        cursor = conn.cursor()
        cursor.execute("select distinct NationalDexID, PokemonName from NationalDex")
        national_dex_pokemon: list = cursor.fetchall()
        conn.close()
        return national_dex_pokemon

    def _pokemon_selected(self, event):
        selected_pokemon = self.pkmn_tree.focus()
        print(self.pkmn_tree.item(selected_pokemon)["values"][0])


def _db_update_icon_normal():
    conn = sqlite3.connect("DB/PokeDexDB.sqlite3")
    cursor = conn.cursor()
    image_blob: bytes = image_to_blob(IMAGE)
    cursor.execute("update NationalDex set IconNormal = ? where PokemonID = ?", (image_blob, PKMN_ID))
    conn.commit()
    conn.close()


def _db_update_icon_shiny():
    conn = sqlite3.connect("DB/PokeDexDB.sqlite3")
    cursor = conn.cursor()
    image_blob: bytes = image_to_blob(IMAGE)
    cursor.execute("update NationalDex set IconShiny = ? where PokemonID = ?", (image_blob, PKMN_ID))
    conn.commit()
    conn.close()


def db_get_icon() -> bytes:
    conn = sqlite3.connect("DB/PokeDexDB.sqlite3")
    cursor = conn.cursor()
    cursor.execute("select IconNormal from NationalDex where PokemonID = ?", (PKMN_ID,))
    img_data = cursor.fetchone()[0]
    conn.close()
    return img_data


def main():
    pokedex_db: str = "DB/PokeDexDB.sqlite3"
    dex_builder = RegionalDexBuilder(pokedex_db)
    dex_builder.create_main_window()
    # create_main_window()
    # _db_update_icon_normal()
    # _db_update_icon_shiny()


if __name__ == "__main__":
    main()
