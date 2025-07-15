# Python Libraries
from tkinter import Tk, LEFT, BOTH
from tkinter.ttk import Notebook, Style

# Local Libraries
from db.db import PokedexDB
from ui.viewer_frame import ViewerFrame
from ui.editor_frame import EditorFrame

# Global Declarations
TITLE: str = "PyPokédex"
VERSION: str = "1.0.3"


class PokedexApp(Tk):
    def __init__(self):
        # Database
        super().__init__()

        self.minsize(600, 625)


        # Configure styles
        style: Style = Style()
        style.theme_use("clam")
        style.configure("pink.TFrame", background="pink")
        style.configure("blue.Horizontal.TProgressbar", foreground="blue", background="blue")
        style.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
        style.configure("yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        style.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
        style.configure("Ability.TLabel", borderwidth=1, relief="solid", padding=5, foreground="black")
        style.configure("HiddenAbility.TLabel", borderwidth=1, relief="solid", padding=5, foreground="gray")

        self.title(f"{TITLE} - {VERSION}")
        self.bind("<Configure>", self._on_resize)

        self.db: PokedexDB = PokedexDB()

        self.tab_menu: Notebook = Notebook(self)
        self.viewer_frame: ViewerFrame = ViewerFrame()
        self.editor_frame: EditorFrame = EditorFrame()

        #
        self.pokedex_headers: dict = {}

        # Start application
        self.create_widgets()

    def create_widgets(self) -> None:
        self.geometry("640x640")
        # self.resizable(False, False)

        self.tab_menu.add(self.viewer_frame, text="Pokédex Viewer")
        self.tab_menu.add(self.editor_frame, text="Pokédex Editor")

        self.viewer_frame.pokemon_tree.bind("<<TreeviewSelect>>", self._on_pokemon_changed)
        self.viewer_frame.form_tree.bind("<<TreeviewSelect>>", self._on_form_changed)
        self.viewer_frame.game_var.trace("w", self._on_game_changed)
        self.viewer_frame.dex_var.trace("w", self._on_dex_changed)
        self.viewer_frame.shiny.trace("w", self._on_shiny_changed)
        games: list = self.db.get_games()
        self.viewer_frame.refresh_games(games)

        # Frame placement
        self.tab_menu.pack(side=LEFT, fill=BOTH, expand=True)

    # Event Handlers
    def _on_resize(self, event):
        self.tab_menu.config(width=event.width, height=event.height)

    def _on_pokemon_changed(self, event) -> None:
        game: str = self.viewer_frame.get_game()
        dex: str = self.viewer_frame.get_dex()
        national_dex_id: int = self.viewer_frame.get_national_dex_id()
        forms: list = self.db.get_forms(game, dex, national_dex_id)
        self.viewer_frame.refresh_form_tree(forms)

    def _on_form_changed(self, event) -> None:
        pokemon_id: int = self.viewer_frame.get_pokemon_id()
        shiny: bool = bool(self.viewer_frame.shiny.get())
        type_set_id: int = self.pokedex_headers[pokemon_id][0]
        stat_set_id: int = self.pokedex_headers[pokemon_id][1]
        ability_set_id: int = self.pokedex_headers[pokemon_id][2]
        game_id: int = self.pokedex_headers[pokemon_id][3]

        portrait_icon: bytes = self.db.get_portrait_icon(pokemon_id, shiny)
        type_icons: tuple = self.db.get_type_icons(type_set_id)
        stats: list = self.db.get_stats(stat_set_id)
        max_stats: tuple = self.db.get_max_stats(game_id)
        abilities: tuple = self.db.get_abilities(ability_set_id)

        self.viewer_frame.refresh_portrait_icon(portrait_icon)
        self.viewer_frame.refresh_type_icons(type_icons)
        self.viewer_frame.refresh_max_stats(max_stats)
        self.viewer_frame.refresh_stats(stats)
        self.viewer_frame.refresh_abilities(abilities)

    def _on_game_changed(self, *args) -> None:
        game: str = self.viewer_frame.get_game()

        # Refresh dex data
        dexes: list = self.db.get_dexes(game)
        self.viewer_frame.refresh_dexes(dexes)

    def _on_dex_changed(self, *args) -> None:
        game: str = self.viewer_frame.get_game()
        dex: str = self.viewer_frame.get_dex()

        # Refresh Pokémon list
        self.pokedex_headers = self.db.get_pokedex_headers(game, dex)
        pokemon: list = self.db.get_pokemon(game, dex)
        self.viewer_frame.refresh_pokemon_tree(pokemon)

    def _on_shiny_changed(self, *args) -> None:
        pokemon_id: int = self.viewer_frame.get_pokemon_id()
        shiny: bool = bool(self.viewer_frame.shiny.get())
        portrait_icon: bytes = self.db.get_portrait_icon(pokemon_id, shiny)
        self.viewer_frame.refresh_portrait_icon(portrait_icon)


if __name__ == "__main__":
    app: PokedexApp = PokedexApp()
    app.mainloop()
