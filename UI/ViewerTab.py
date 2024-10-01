from tkinter import StringVar, END, VERTICAL, NS, PhotoImage, E
from tkinter.ttk import Frame, Label, Progressbar, Treeview, Scrollbar, Entry, OptionMenu
from typing import Optional


class ViewerTab:
    def __init__(self, frame: Frame) -> None:
        self.viewer_frame: Frame = frame

        # Subframes to contain controls.
        self.selector_subframe: Optional[Frame] = None
        self.heading_subframe: Optional[Frame] = None
        self.stats_subframe: Optional[Frame] = None

        # Control headers.
        self.game_var: StringVar = StringVar()
        self.game_selector: Optional[OptionMenu] = None
        self.dex_var: StringVar = StringVar()
        self.dex_selector: Optional[OptionMenu] = None

        # Refresh primary type
        self.primary_type_icon: Optional[PhotoImage] = None
        self.primary_type_icon_lbl: Optional[Label] = None

        # Refresh secondary type
        self.secondary_type_icon: Optional[PhotoImage] = None
        self.secondary_type_icon_lbl: Optional[Label] = None

        self.icon: Optional[PhotoImage] = None
        self.icon_lbl: Optional[Label] = None
        self.search_label: Optional[Label] = None
        self.search_var: StringVar = StringVar()
        self.search_bar: Optional[Entry] = None
        self.selector: Optional[Treeview] = None
        self.selector_scrollbar: Optional[Scrollbar] = None
        self.stat_labels: list = []
        self.stat_bars: list = []

        # List to store passed Pokémon data.
        self.selector_data: list = []

        # Create widgets.
        self.create_selector_subframe()
        self.create_heading_subframe()
        self.create_stats_subframe()

    # Create subframe to hold Pokémon selection tree and related controls.
    def create_selector_subframe(self):
        # Subframe to contain controls
        self.selector_subframe = Frame(self.viewer_frame)

        # Control declarations
        self.game_selector = OptionMenu(self.selector_subframe, self.game_var)
        self.dex_selector = OptionMenu(self.selector_subframe, self.dex_var)
        self.search_label = Label(self.selector_subframe, text="Search:")
        self.search_bar = Entry(self.selector_subframe, textvariable=self.search_var)
        self.selector: Treeview = Treeview(
            self.selector_subframe,
            columns=["PokemonID", "NationalDexNo", "PokemonName"],
            displaycolumns=["NationalDexNo", "PokemonName"],
            show="headings",

        )
        self.selector_scrollbar: Scrollbar = Scrollbar(
            self.selector_subframe,
            orient=VERTICAL,
            command=self.selector.yview
        )

        # Control configurations
        self.selector.column("NationalDexNo", width=30, minwidth=30)
        self.selector.heading("NationalDexNo", text="#")
        self.selector.heading("PokemonName", text="Pokemon")
        self.selector.configure(yscrollcommand=self.selector_scrollbar.set)
        self.search_var.trace("w", self.on_search_var_changed)
        self.dex_var.set("Not Selected")

        # Place controls
        self.game_selector.grid(column=0, row=0, columnspan=2)
        self.dex_selector.grid(column=0, row=1, columnspan=2)
        self.search_label.grid(column=0, row=2, pady=10)
        self.search_bar.grid(column=1, row=2, pady=10, ipadx=30, columnspan=2)
        self.selector.grid(column=0, row=3, padx=10, ipady=50, columnspan=4)
        self.selector_scrollbar.grid(column=4, row=3, sticky=NS)

        # Place Subframe
        self.selector_subframe.grid(column=0, row=0, rowspan=2)

    def create_heading_subframe(self):
        # Subframe to contain controls.
        self.heading_subframe = Frame(self.viewer_frame)

        # Control declarations/placement.
        self.icon_lbl = Label(self.heading_subframe)
        self.primary_type_icon_lbl = Label(self.heading_subframe)
        self.secondary_type_icon_lbl = Label(self.heading_subframe)

        # Place Controls.
        self.icon_lbl.grid(column=0, row=0, columnspan=2)
        self.primary_type_icon_lbl.grid(column=0, row=1)
        self.secondary_type_icon_lbl.grid(column=1, row=1)

        # Place Subframe.
        self.heading_subframe.grid(column=1, row=0, sticky="n")

    # Create subframe to hold stat-related UI elements.
    def create_stats_subframe(self):
        # Subframe to contain controls.
        self.stats_subframe = Frame(self.viewer_frame)

        # Control declarations/placement.
        labels: list = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]

        for i, label in enumerate(labels):
            stat_label: Label = Label(self.stats_subframe, text=labels[i])
            stat_label.grid(column=0, row=i)
            self.stat_labels.append(stat_label)

            stat_bar: Progressbar = Progressbar(
                self.stats_subframe,
                style="TProgressbar",
                length=200,
                mode='determinate'
            )
            stat_bar.grid(column=1, row=i)
            self.stat_bars.append(stat_bar)

        # Place Subframe.
        self.stats_subframe.grid(column=1, row=1)

    def refresh_type_icons(self, type_icons: tuple):
        # Refresh primary type
        self.primary_type_icon = PhotoImage(data=type_icons[0])
        self.primary_type_icon_lbl.config(image=self.primary_type_icon)

        # Refresh secondary type
        self.secondary_type_icon = PhotoImage(data=type_icons[1])
        self.secondary_type_icon_lbl.config(image=self.secondary_type_icon)

    # Set stat bar data to passed list of stats.
    def refresh_stats(self, stats: list) -> None:
        for i, stat_bar in enumerate(self.stat_bars):
            stat_bar["value"] = stats[i]

    def refresh_icon(self, icon_data: bytes) -> None:
        self.icon = PhotoImage(data=icon_data)
        self.icon_lbl.config(image=self.icon)

    def focus_first(self) -> None:
        self.selector.focus_set()
        children: tuple = self.selector.get_children()
        if children:
            self.selector.focus(children[0])
            self.selector.selection_set(children[0])

    # Search Pokémon in selector by either name or dex number.
    def search_pokemon(self, term: str):
        self.selector.delete(*self.selector.get_children())
        for values in self.selector_data:
            if term in values[2].lower() or term == str(values[1]):
                self.selector.insert("", END, values=values)
        self.focus_first()
        self.search_bar.focus_set()

    # Returns Pokémon ID of current selection.
    def get_pokemon_id(self) -> int:
        pokemon: str = self.selector.focus()
        if pokemon:
            pokemon_id: int = self.selector.item(pokemon)["values"][0]
        else:
            pokemon_id: int = 0
        return pokemon_id

    # Returns game name for current selection.
    def get_game(self) -> str:
        game: str = self.game_var.get()
        if not game:
            game += "Red/Blue/Yellow"
        return game

    # Returns dex name for current selection.
    def get_dex(self) -> str:
        dex: str = self.dex_var.get()
        if not dex:
            dex += "Kanto Pokedex"
        return dex

    # Flushes selector values, and replaces them with the passed Pokémon data.
    def refresh_pokemon(self, pokemon: list) -> None:
        # Store passed data
        self.selector_data = pokemon

        # Delete items from tree
        self.selector.delete(*self.selector.get_children())

        # Populate Tree
        for values in self.selector_data:
            self.selector.insert("", END, values=values)

        self.on_search_var_changed()
        self.focus_first()

    def refresh_games(self, games: list):
        self.game_selector["menu"].delete(0, END)
        if games:
            for game in games:
                self.game_selector["menu"].add_command(label=game, command=lambda g=game: self.game_var.set(g))
            self.game_var.set(games[0])

    def refresh_dexes(self, dexes: list):
        self.dex_selector["menu"].delete(0, END)
        if dexes:
            for dex in dexes:
                self.dex_selector["menu"].add_command(label=dex, command=lambda d=dex: self.dex_var.set(d))
            self.dex_var.set(dexes[0])

    # Event handlers
    def on_search_var_changed(self, *args):
        term: str = self.search_var.get().lower()
        self.search_pokemon(term)
