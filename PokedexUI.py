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
        self.pokemon_selector = None
        self.pkmn_icon_lbl = None
        self.stat_bars: list = []

        # Data Variables
        self.games: dict = self.db.get_games()

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
        self.dex_frame = ttk.Frame(root)
        self.pokemon_frame = ttk.Frame(root)
        self.stats_frame = ttk.Frame(root)

        self._set_dex_controls()
        self._set_pokemon_controls()
        self._set_stat_controls()

        # Main control placement
        self.pkmn_icon_lbl = tk.Label(root)
        self.pkmn_icon_lbl.grid(column=1, row=0)

        # Frame placement
        self.dex_frame.grid(column=0, row=0)
        self.pokemon_frame.grid(column=0, row=1)
        self.stats_frame.grid(column=1, row=1)

        self._refresh_pkmn_list()

        # Start loop
        root.mainloop()

    def _set_dex_controls(self):
        self.cur_game: tk.StringVar = tk.StringVar(self.dex_frame, list(self.games.keys())[0])
        self.game_selector = ttk.OptionMenu(self.dex_frame, self.cur_game, *self.games.keys(),
                                            command=self._on_game_selected)
        self.game_selector.grid(column=0, row=0)

    def _set_pokemon_controls(self):
        self.pokemon_selector = ttk.Treeview(
            self.pokemon_frame,
            columns=["PokemonID", "NationalDexNo", "PokemonName"],
            displaycolumns=["NationalDexNo", "PokemonName"],
            show="headings")

        self.pokemon_selector.column("NationalDexNo", width=30, minwidth=30)
        self.pokemon_selector.heading("NationalDexNo", text="#")
        self.pokemon_selector.heading("PokemonName", text="Pokemon")
        self.pokemon_selector.bind("<<TreeviewSelect>>", self._on_pokemon_selected)
        self.pokemon_selector.grid(column=0, row=0, rowspan=2)

    def _set_stat_controls(self) -> None:
        i: int = 0
        while i < 6:
            stat_bar = ttk.Progressbar(self.stats_frame, style="TProgressbar", length=200, mode='determinate')
            stat_bar.grid(column=0, row=i)
            self.stat_bars.append(stat_bar)
            i += 1

    def _refresh_pkmn_stats(self) -> None:
        pkmn_stats: list = self.db.get_pkmn_stats(self.cur_pokemon_id)
        i: int = 0
        while i < 6:
            self.stat_bars[i]["value"] = pkmn_stats[i]
            i += 1

    def _refresh_pkmn_list(self) -> None:
        # Delete items from tree
        self.pokemon_selector.delete(*self.pokemon_selector.get_children())

        # Populate Tree
        for pokemon in self.db.get_pkmn_national_dex():
            self.pokemon_selector.insert("", tk.END, values=pokemon)

        # Focus first item
        self.pokemon_selector.focus_set()
        children: tuple = self.pokemon_selector.get_children()
        if children:
            self.pokemon_selector.focus(children[0])
            self.pokemon_selector.selection_set(children[0])

    def _refresh_pkmn_icon(self) -> None:
        icon_data: bytes = self.db.get_pkmn_icon(self.cur_pokemon_id, SHINY)
        self.pkmn_icon = tk.PhotoImage(data=icon_data)
        self.pkmn_icon_lbl.config(image=self.pkmn_icon)

    def _update_cur_pkmn_id(self) -> None:
        selected_pokemon = self.pokemon_selector.focus()
        self.cur_pokemon_id = self.pokemon_selector.item(selected_pokemon)["values"][0]

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
        game_id: int = self.games[event]


def main():
    pokedex = PokedexApp()


if __name__ == "__main__":
    main()
