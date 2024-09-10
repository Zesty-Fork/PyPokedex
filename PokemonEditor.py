# Python Libraries
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

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


class PokemonEditor:
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
        self.split_genders_btn = tk.Button(root, text="Split Gendered Forms", command=self._on_split_genders_clicked)
        self.add_gigantamax_btn = tk.Button(root, text="Add Gigantamax Form", command=self._on_gigantamax_clicked)

        # Bindings
        self.icon_normal_lbl.bind("<Button-1>", self._on_icon_normal_clicked)
        self.icon_shiny_lbl.bind("<Button-1>", self._on_icon_shiny_clicked)

        # Grid controls
        self.pkmn_tree.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.icon_normal_lbl.pack(side=tk.LEFT)
        self.icon_shiny_lbl.pack(side=tk.LEFT)
        self.split_genders_btn.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.add_gigantamax_btn.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self._refresh_pokemon_list()

        # Start loop
        root.mainloop()

    def _refresh_pokemon_list(self) -> None:
        # Delete items from tree
        self.pkmn_tree.delete(*self.pkmn_tree.get_children())

        # Populate Tree
        for pokemon in self.db.get_pkmn_national_dex():
            self.pkmn_tree.insert("", tk.END, values=pokemon)

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

    def _on_split_genders_clicked(self) -> None:
        self.db.split_gender_forms(self.cur_pokemon_id)
        self._refresh_pokemon_list()

    def _on_gigantamax_clicked(self):
        self.db.add_gigantamax_form(self.cur_pokemon_id)
        self._refresh_pokemon_list()

def main():
    dex_builder = PokemonEditor()


if __name__ == "__main__":
    main()
