# Python Libraries
from tkinter import TclError, Tk
from tkinter.ttk import Frame, Notebook, Style
from typing import Optional

# Local Libraries
from DB.PokeDB import PokeDexDB
from UI.ViewerTab import ViewerTab

# Global Declarations
TITLE: str = "PyPokedex"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind
SHINY: bool = False


class PokedexApp:
    def __init__(self):
        # Database
        self.db: PokeDexDB = PokeDexDB()

        self.tab_menu: Optional[Notebook] = None
        self.tab1: Optional[Frame] = None
        self.tab2: Optional[Frame] = None
        self.viewer_tab: Optional[ViewerTab] = None

        #
        self.pokedex_headers: dict = {}

        # Start application
        self.create_main_window()

    def create_main_window(self) -> None:
        root = Tk()
        root.title(TITLE)
        root.geometry("800x580")
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

        self.viewer_tab = ViewerTab(self.tab1)
        # self.editor_tab: Frame = Frame(self.tab_menu)

        self.viewer_tab.pokemon_tree.bind("<<TreeviewSelect>>", self.on_pokemon_changed)
        self.viewer_tab.form_tree.bind("<<TreeviewSelect>>", self.on_form_changed)
        self.viewer_tab.game_var.trace("w", self.on_game_changed)
        self.viewer_tab.dex_var.trace("w", self.on_dex_changed)
        self.viewer_tab.shiny.trace("w", self.on_shiny_changed)
        games: list = self.db.get_games()
        self.viewer_tab.refresh_games(games)

        # Frame placement
        self.tab_menu.grid(column=0, row=0)

        # Start loop
        root.mainloop()

    # Event Handlers
    def on_pokemon_changed(self, event):
        game: str = self.viewer_tab.get_game()
        dex: str = self.viewer_tab.get_dex()
        national_dex_id: int = self.viewer_tab.get_national_dex_id()
        forms: list = self.db.get_forms(game, dex, national_dex_id)
        self.viewer_tab.refresh_form_tree(forms)

    def on_form_changed(self, event):
        pokemon_id: int = self.viewer_tab.get_pokemon_id()
        shiny: bool = bool(self.viewer_tab.shiny.get())
        type_set_id: int = self.pokedex_headers[pokemon_id][0]
        stat_set_id: int = self.pokedex_headers[pokemon_id][1]
        ability_set_id: int = self.pokedex_headers[pokemon_id][2]
        game_id: int = self.pokedex_headers[pokemon_id][3]

        portrait_icon: bytes = self.db.get_pkmn_icon(pokemon_id, shiny)
        type_icons: tuple = self.db.get_type_icons(type_set_id)
        stats: list = self.db.get_stats(stat_set_id)
        max_stats: tuple = self.db.get_max_stats(game_id)
        abilities: tuple = self.db.get_abilities(ability_set_id)

        self.viewer_tab.refresh_portrait_icon(portrait_icon)
        self.viewer_tab.refresh_type_icons(type_icons)
        self.viewer_tab.refresh_max_stats(max_stats)
        self.viewer_tab.refresh_stats(stats)
        self.viewer_tab.refresh_abilities(abilities)

    def on_game_changed(self, *args):
        game: str = self.viewer_tab.get_game()

        # Refresh dex data
        dexes: list = self.db.get_dexes(game)
        self.viewer_tab.refresh_dexes(dexes)

    def on_dex_changed(self, *args):
        game: str = self.viewer_tab.get_game()
        dex: str = self.viewer_tab.get_dex()

        # Refresh Pokémon list
        self.pokedex_headers = self.db.get_pokedex_headers(game, dex)
        pokemon: list = self.db.get_pokemon(game, dex)
        self.viewer_tab.refresh_pokemon_tree(pokemon)

    def on_shiny_changed(self, *args):
        pokemon_id: int = self.viewer_tab.get_pokemon_id()
        shiny: bool = bool(self.viewer_tab.shiny.get())
        portrait_icon: bytes = self.db.get_pkmn_icon(pokemon_id, shiny)
        self.viewer_tab.refresh_portrait_icon(portrait_icon)



def main():
    app = PokedexApp()


if __name__ == "__main__":
    main()
