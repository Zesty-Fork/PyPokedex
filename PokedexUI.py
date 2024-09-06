# Python Libraries
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import shutil

# Local Libraries
from DB.PokeDB import PokeDexDB

# Global Declarations
TITLE: str = "RegionalDexBuilder"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind


def image_to_blob(image_path: str) -> bytes:
    blob: bytes = b""
    with open(image_path, "rb") as image_file:
        blob = image_file.read()
    return blob


class RegionalDexBuilder:
    def __init__(self):
        # Database
        self.db: PokeDexDB = PokeDexDB()

        # Selection Variables
        self.cur_pokemon_id: int = 1

        # Control Variables
        self.pkmn_tree = None
        self.icon_normal_lbl = None
        self.icon_shiny_lbl = None

        self._create_main_window()

    def _create_main_window(self):
        root = tk.Tk()
        root.title(TITLE)
        root.geometry("800x600")
        root.resizable(False, False)

        # Remove the minimize/maximize button (Windows only)
        try:
            root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")

        columns: list = ["PokemonID", "NationalDexNo", "PokemonName"]
        displaycolumns: list = ["NationalDexNo", "PokemonName"]
        self.pkmn_tree = ttk.Treeview(root, columns=columns, displaycolumns=displaycolumns, show="headings")
        self.pkmn_tree.column("NationalDexNo", width=30, minwidth=30)

        # Define headings
        self.pkmn_tree.heading("NationalDexNo", text="#")
        self.pkmn_tree.heading("PokemonName", text="Pokemon")

        # Control variable declarations
        self.pkmn_tree.bind("<<TreeviewSelect>>", self._on_pokemon_selected)
        self.icon_normal_lbl = tk.Label(root, width=112, height=112)
        self.icon_shiny_lbl = tk.Label(root, width=112, height=112)

        # Bindings
        self.icon_normal_lbl.bind("<Button-1>", self._on_icon_normal_clicked)
        self.icon_shiny_lbl.bind("<Button-1>", self._on_icon_shiny_clicked)

        # Pack controls
        self.pkmn_tree.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.icon_normal_lbl.pack(side=tk.LEFT)
        self.icon_shiny_lbl.pack(side=tk.LEFT)

        # Populate selection list
        for pokemon in self.db.get_national_dex_pokemon():
            self.pkmn_tree.insert("", tk.END, values=pokemon)

        # Start loop
        root.mainloop()

    # Event Handlers
    def _on_pokemon_selected(self, event):
        selected_pokemon = self.pkmn_tree.focus()
        self.cur_pokemon_id = self.pkmn_tree.item(selected_pokemon)["values"][0]

        icon_normal_data: bytes = self.db.get_icon_normal(self.cur_pokemon_id)
        if icon_normal_data:
            self.icon_normal = tk.PhotoImage(data=icon_normal_data)
            self.icon_normal_lbl.config(image=self.icon_normal, width=112, height=112)
        else:
            self.icon_normal = tk.PhotoImage(file="Placeholder.png")
            self.icon_normal_lbl.config(image=self.icon_normal, width=112, height=112)

        icon_shiny_data: bytes = self.db.get_icon_shiny(self.cur_pokemon_id)
        if icon_shiny_data:
            self.icon_shiny = tk.PhotoImage(data=icon_shiny_data)
            self.icon_shiny_lbl.config(image=self.icon_shiny, width=112, height=112)

        else:
            self.icon_shiny = tk.PhotoImage(file="Placeholder.png")
            self.icon_shiny_lbl.config(image=self.icon_shiny, width=112, height=112)

    def _on_icon_normal_clicked(self, event) -> None:
        filename: str = tk.filedialog.askopenfilename()
        if filename:
            image_blob: bytes = image_to_blob(filename)
            self.db.update_icon_normal(self.cur_pokemon_id, image_blob)
            self._on_pokemon_selected("event")

    def _on_icon_shiny_clicked(self, event) -> None:
        filename: str = tk.filedialog.askopenfilename()
        if filename:
            image_blob: bytes = image_to_blob(filename)
            self.db.update_icon_shiny(self.cur_pokemon_id, image_blob)
            self._on_pokemon_selected("event")


def main():
    dex_builder = RegionalDexBuilder()
    import sqlite3
    for filename in os.listdir("Pokémon HOME/Pokémon Icons"):
        if filename.endswith(".png"):
            if filename.split("_")[4] == "mf" and filename.split("_")[5] == "n":
                national_dex_id: int = int(filename.split("_")[2])
                form_id: int = int(filename.split("_")[3])
                image_blob: bytes = image_to_blob(f"Pokémon HOME/Pokémon Icons/{filename}")
                conn = sqlite3.connect("DB/PokeDB.sqlite3")
                cursor = conn.cursor()
                if form_id == 0:
                    if filename.endswith("n.png"):
                        cursor.execute("""
                            update NationalDex
                            set IconNormal = ?
                            where NationalDexID = ?
                                and FormID = 1
                        """, (image_blob, national_dex_id))
                    elif filename.endswith("r.png"):
                        cursor.execute("""
                            update NationalDex
                            set IconShiny = ?
                            where NationalDexID = ?
                                and FormID = 1
                        """, (image_blob, national_dex_id))
                    conn.commit()
                    shutil.move(f"Pokémon HOME/Pokémon Icons/{filename}", f"Pokémon HOME/Processed/{filename}")


if __name__ == "__main__":
    main()
