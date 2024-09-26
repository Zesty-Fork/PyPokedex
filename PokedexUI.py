# Python Libraries
from tkinter import END, Label, PhotoImage, StringVar, TclError, Tk
from tkinter.ttk import Frame, OptionMenu, Notebook

# Local Libraries
from DB.PokeDB import PokeDexDB
from UI.ViewerTab import ViewerTab

# Global Declarations
TITLE: str = "Pokedex"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind
SHINY: bool = True


class PokedexApp:
    def __init__(self):
        # Database
        self.db: PokeDexDB = PokeDexDB()

        # Control Variables
        self.pkmn_icon_lbl = None

        # Start application
        self._create_main_window()

    def _create_main_window(self):
        root = Tk()
        root.title(TITLE)
        root.geometry("600x650")
        root.resizable(False, False)

        # Remove the minimize/maximize button (Windows only)
        try:
            root.attributes("-toolwindow", True)
        except TclError:
            print("Not supported on your platform")

        self.tab_menu: Notebook = Notebook(root)
        self.tab1: Frame = Frame(self.tab_menu)
        self.tab2: Frame = Frame(self.tab_menu)

        self.tab_menu.add(self.tab1, text="Pokedex Viewer")
        self.tab_menu.add(self.tab2, text="Pokedex Editor")

        self.viewer_tab: ViewerTab = ViewerTab(self.tab1)
        # self.editor_tab: Frame = Frame(self.tab_menu)

        # Frame variables
        self.dex_frame = Frame(root)

        self._set_dex_controls()

        # Main control placement
        self.pkmn_icon_lbl = Label(root)
        self.pkmn_icon_lbl.grid(column=1, row=0)

        # Frame placement
        self.dex_frame.grid(column=0, row=0)
        self.tab_menu.grid(column=0, row=1)

        self.viewer_tab.selector.bind("<<TreeviewSelect>>", self._on_pokemon_selected)

        # Start loop
        root.mainloop()

    def _set_dex_controls(self):
        self.game_var: StringVar = StringVar(self.dex_frame, "Not Selected")
        self.dex_var: StringVar = StringVar(self.dex_frame, "Not Selected")

        self.game_selector = OptionMenu(self.dex_frame, self.game_var)
        self.dex_selector = OptionMenu(self.dex_frame, self.dex_var)

        self.game_var.trace("w", self._on_game_changed)
        self.dex_var.trace("w", self._on_dex_changed)

        self.game_selector.grid(column=0, row=0)
        self.dex_selector.grid(column=1, row=0)

        self._refresh_games()

    def _refresh_icon(self) -> None:
        icon_data: bytes = self.db.get_pkmn_icon(SHINY)
        self.pkmn_icon = PhotoImage(data=icon_data)
        self.pkmn_icon_lbl.config(image=self.pkmn_icon)

    # Event Handlers
    def _on_pokemon_selected(self, event):
        pokemon_id: int = self.viewer_tab.get_pokemon_id()
        self.db.set_pokemon_id(pokemon_id)
        self._refresh_icon()
        self.viewer_tab.refresh_stats(self.db.get_stats())

    def _on_form_selected(self, event):
        pass

    def _on_game_changed(self, *args):
        self.db.cur_game = self.game_var.get()
        self.dex_var.set("Not Selected")
        self._refresh_dexes()

    def _on_dex_changed(self, *args):
        self.db.cur_dex = self.dex_var.get()
        pokemon: list = self.db.get_pokemon()
        self.viewer_tab.refresh_pokemon(pokemon)

    def _refresh_games(self):
        self.game_selector["menu"].delete(0, END)
        games: list = self.db.get_games()
        if games:
            for game in games:
                self.game_selector["menu"].add_command(label=game, command=lambda g=game: self.game_var.set(g))
            self.game_var.set(games[0])

    def _refresh_dexes(self):
        self.dex_selector["menu"].delete(0, END)
        dexes: list = self.db.get_dexes()
        if dexes:
            for dex in dexes:
                self.dex_selector["menu"].add_command(label=dex, command=lambda d=dex: self.dex_var.set(d))
            self.dex_var.set(dexes[0])


def main():
    app = PokedexApp()


if __name__ == "__main__":
    main()
