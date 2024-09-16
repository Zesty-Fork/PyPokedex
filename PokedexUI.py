# Python Libraries
import tkinter as tk
from tkinter import ttk

# Local Libraries
from DB.PokeDB import PokeDexDB

# Global Declarations
TITLE: str = "RegionalDexBuilder"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind
SHINY: bool = True


class PokedexApp:
    def __init__(self):
        # Database
        self.db: PokeDexDB = PokeDexDB()

        # Selection Variables
        self.cur_pokemon_id: int = 1

        # Control Variables
        self.pkmn_tree = None
        self.pkmn_icon_lbl = None
        self.pkmn_stats_ctrls: list = []

        # Start application
        self._create_main_window()

    def _create_main_window(self):
        root = tk.Tk()
        root.title(TITLE)
        root.geometry("600x650")
        root.resizable(False, False)

        # Remove the minimize/maximize button (Windows only)
        try:
            root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")

        # Stats frame variables
        self.pkmn_stats_frame = ttk.Frame(root)
        self._set_pkmn_stat_controls()

        # Tree view control
        columns: list = ["PokemonID", "NationalDexNo", "PokemonName"]
        displaycolumns: list = ["NationalDexNo", "PokemonName"]
        self.pkmn_tree = ttk.Treeview(root, columns=columns, displaycolumns=displaycolumns, show="headings")
        self.pkmn_tree.column("NationalDexNo", width=30, minwidth=30)

        # Define headings
        self.pkmn_tree.heading("NationalDexNo", text="#")
        self.pkmn_tree.heading("PokemonName", text="Pokemon")

        # Pokemon games option menu
        self.pkmn_games: dict = self.db.get_pkmn_games()
        self.cur_game: tk.StringVar = tk.StringVar(root, list(self.pkmn_games.keys())[0])
        self.pkmn_game_om = tk.OptionMenu(root, self.cur_game, *self.pkmn_games.keys(), command=self._on_game_selected)
        self.pkmn_icon_lbl = tk.Label(root)

        # Game dex option menu

        # Bindings
        self.pkmn_tree.bind("<<TreeviewSelect>>", self._on_pokemon_selected)

        # Main control placement
        self.pkmn_game_om.grid(column=0, row=0)
        self.pkmn_tree.grid(column=0, row=1, rowspan=2)
        self.pkmn_icon_lbl.grid(column=1, row=0)

        # Stats frame placement
        self.pkmn_stats_frame.grid(column=1, row=1)

        self._refresh_pkmn_list()

        # Start loop
        root.mainloop()

    def _set_pkmn_stat_controls(self) -> None:
        i: int = 0
        while i < 6:
            stat_pb = ttk.Progressbar(self.pkmn_stats_frame, style="TProgressbar", length=200, mode='determinate')
            stat_pb.grid(column=0, row=i)
            self.pkmn_stats_ctrls.append(stat_pb)
            i += 1

    def _refresh_pkmn_stats(self) -> None:
        pkmn_stats: list = self.db.get_pkmn_stats(self.cur_pokemon_id)
        i: int = 0
        while i < 6:
            self.pkmn_stats_ctrls[i]["value"] = pkmn_stats[i]
            i += 1

    def _refresh_pkmn_list(self) -> None:
        # Delete items from tree
        self.pkmn_tree.delete(*self.pkmn_tree.get_children())

        # Populate Tree
        for pokemon in self.db.get_pkmn_national_dex():
            self.pkmn_tree.insert("", tk.END, values=pokemon)

        # Focus first item
        self.pkmn_tree.focus_set()
        children: tuple = self.pkmn_tree.get_children()
        if children:
            self.pkmn_tree.focus(children[0])
            self.pkmn_tree.selection_set(children[0])

    def _refresh_pkmn_icon(self) -> None:
        icon_data: bytes = self.db.get_pkmn_icon(self.cur_pokemon_id, SHINY)
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

    def _on_game_selected(self, event):
        game_id: int = self.pkmn_games[event]



def main():
    pokedex = PokedexApp()


if __name__ == "__main__":
    main()
