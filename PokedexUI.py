# Python Libraries
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# Local Libraries
from DB.PokeDB import PokeDexDB

# Global Declarations
TITLE: str = "RegionalDexBuilder"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind
SHINY: bool = True


def image_to_blob(image_path: str) -> bytes:
    blob: bytes = b""
    with open(image_path, "rb") as image_file:
        blob = image_file.read()
    return blob


class PokedexApp:
    def __init__(self):
        # Database
        self.db: PokeDexDB = PokeDexDB()

        # Selection Variables
        self.cur_pokemon_id: int = 1

        # Control Variables
        self.pkmn_tree = None
        self.pkmn_icon_lbl = None

        # Start application
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

        # Create a style object
        style = ttk.Style()

        # Configure the style for the progress bar
        style.configure("TProgressbar", troughcolor='white', background='blue', thickness=30)

        # Stats frame variables
        self.pkmn_stats_frame = ttk.Frame(root)
        self.pkmn_hp_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate',
                                          maximum=800)
        self.pkmn_atk_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')
        self.pkmn_def_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')
        self.pkmn_spa_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')
        self.pkmn_spd_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')
        self.pkmn_spe_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')

        # Tree view control
        columns: list = ["PokemonID", "NationalDexNo", "PokemonName"]
        displaycolumns: list = ["NationalDexNo", "PokemonName"]
        self.pkmn_tree = ttk.Treeview(root, columns=columns, displaycolumns=displaycolumns, show="headings")
        self.pkmn_tree.column("NationalDexNo", width=30, minwidth=30)

        # Define headings
        self.pkmn_tree.heading("NationalDexNo", text="#")
        self.pkmn_tree.heading("PokemonName", text="Pokemon")

        # Control variable declarations
        pkmn_games: list = self.db.get_pkmn_games()
        self.pkmn_game_om = tk.OptionMenu(root, *pkmn_games)
        self.pkmn_icon_lbl = tk.Label(root)

        # Bindings
        self.pkmn_tree.bind("<<TreeviewSelect>>", self._on_pokemon_selected)

        # Main control placement
        self.pkmn_game_om.grid(column=0, row=0)
        self.pkmn_tree.grid(column=0, row=1, rowspan=2)
        self.pkmn_icon_lbl.grid(column=1, row=0)

        # Stats frame placement
        self.pkmn_stats_frame.grid(column=1, row=1)
        self.pkmn_hp_pb.grid(column=0, row=0)
        self.pkmn_atk_pb.grid(column=0, row=1)
        self.pkmn_def_pb.grid(column=0, row=2)
        self.pkmn_spa_pb.grid(column=0, row=3)
        self.pkmn_spd_pb.grid(column=0, row=4)
        self.pkmn_spe_pb.grid(column=0, row=5)

        self._refresh_pkmn_list()

        self.pkmn_tree.focus_set()
        children: tuple = self.pkmn_tree.get_children()
        if children:
            self.pkmn_tree.focus(children[0])
            self.pkmn_tree.selection_set(children[0])

        # Start loop
        root.mainloop()

    def _refresh_pkmn_list(self) -> None:
        # Delete items from tree
        self.pkmn_tree.delete(*self.pkmn_tree.get_children())

        # Populate Tree
        for pokemon in self.db.get_pkmn_national_dex():
            self.pkmn_tree.insert("", tk.END, values=pokemon)

    def _refresh_pkmn_stats(self) -> None:
        pkmn_stats: list = self.db.get_pkmn_stats(self.cur_pokemon_id)
        self.pkmn_hp_pb["value"] = pkmn_stats[0]
        self.pkmn_atk_pb["value"] = pkmn_stats[1]
        self.pkmn_def_pb["value"] = pkmn_stats[2]
        self.pkmn_spa_pb["value"] = pkmn_stats[3]
        self.pkmn_spd_pb["value"] = pkmn_stats[4]
        self.pkmn_spe_pb["value"] = pkmn_stats[5]

    def _refresh_pkmn_icon(self) -> None:
        if SHINY:
            icon_data: bytes = self.db.get_icon_shiny(self.cur_pokemon_id)
        else:
            icon_data: bytes = self.db.get_icon_normal(self.cur_pokemon_id)

        self.pkmn_icon = tk.PhotoImage(data=icon_data)
        self.pkmn_icon_lbl.config(image=self.pkmn_icon)

    def _update_cur_pkmn_id(self) -> None:
        selected_pokemon = self.pkmn_tree.focus()
        self.cur_pokemon_id = self.pkmn_tree.item(selected_pokemon)["values"][0]

        if not self.cur_pokemon_id:
            self.cur_pokemon_id = 0

    # Event Handlers
    def _on_pokemon_selected(self, event):
        self._update_cur_pkmn_id()
        self._refresh_pkmn_icon()
        self._refresh_pkmn_stats()

    def _on_form_selected(self, event):
        pass


def main():
    pokedex = PokedexApp()


if __name__ == "__main__":
    main()
