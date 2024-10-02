from tkinter import StringVar, END, VERTICAL, PhotoImage, LEFT, TOP, X, Y, BOTH, IntVar
from tkinter.ttk import Frame, Label, Progressbar, Treeview, Scrollbar, Entry, OptionMenu, Style, Separator, Checkbutton
from typing import Optional


# Helper function to sort treeview by Pokédex no.
def sort_pokemon_by_dex_no(tree, col, descending):
    data: list = [(int(tree.set(item, col)), item) for item in tree.get_children("")]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, "", index)
    tree.heading(col, command=lambda: sort_pokemon_by_dex_no(tree, col, not descending))
    tree.heading("PokemonName", command=lambda: sort_pokemon_by_name(tree, "PokemonName", False))


# Helper function to sort treeview by Pokémon name.
def sort_pokemon_by_name(tree, col, descending):
    data: list = [(tree.set(item, col), item) for item in tree.get_children("")]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, "", index)
    tree.heading(col, command=lambda: sort_pokemon_by_name(tree, col, not descending))
    tree.heading("NationalDexNo", command=lambda: sort_pokemon_by_dex_no(tree, "NationalDexNo", False))


# Focus first item of passed TreeView object
def focus_first(tree: Treeview) -> None:
    children: tuple = tree.get_children()
    if children:
        tree.focus(children[0])
        tree.selection_set(children[0])


class ViewerTab:
    def __init__(self, frame: Frame) -> None:
        self.viewer_frame: Frame = frame

        # Configure styles
        style: Style = Style()
        style.theme_use('clam')
        style.configure("pink.TFrame", background="pink")
        style.configure("blue.Horizontal.TProgressbar", foreground="blue", background="blue")
        style.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
        style.configure("yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        style.configure("red.Horizontal.TProgressbar", foreground="red", background="red")

        # Subframes to contain controls.
        self.selection_subframe: Optional[Frame] = None
        self.profile_subframe: Optional[Frame] = None
        self.stats_subframe: Optional[Frame] = None

        # Control headers.
        self.game_var: StringVar = StringVar()
        self.game_selector: Optional[OptionMenu] = None
        self.dex_var: StringVar = StringVar()
        self.dex_selector: Optional[OptionMenu] = None
        self.search_var: StringVar = StringVar()
        self.search_bar: Optional[Entry] = None
        self.pokemon_tree: Optional[Treeview] = None
        self.pokemon_tree_scrollbar: Optional[Scrollbar] = None
        self.stat_value_labels: list = []
        self.stat_bars: list = []

        self.shiny: IntVar = IntVar()
        self.shiny_chk: Optional[Checkbutton] = None
        self.form_tree: Optional[Treeview] = None
        self.portrait_icon: Optional[PhotoImage] = None
        self.portrait_icon_lbl: Optional[Label] = None
        self.primary_type_icon: Optional[PhotoImage] = None
        self.primary_type_icon_lbl: Optional[Label] = None
        self.secondary_type_icon: Optional[PhotoImage] = None
        self.secondary_type_icon_lbl: Optional[Label] = None

        # List to store passed Pokémon data.
        self.selector_data: list = []
        self.max_stats: tuple = (0, 0)

        # Create widgets.
        self.create_selection_subframe()
        # Separator(self.viewer_frame, orient=VERTICAL).pack()
        self.create_profile_subframe()
        self.create_stats_subframe()

        # Separator(self.viewer_frame, orient=HORIZONTAL).grid(column=1, row=1, columnspan=3, sticky=EW)

    # Create subframe to hold Pokémon selection tree and related controls.
    def create_selection_subframe(self):
        # Subframe to contain controls
        self.selection_subframe = Frame(self.viewer_frame)
        self.pokemon_tree_grp = Frame(self.selection_subframe)

        # Control declarations
        self.game_selector = OptionMenu(self.selection_subframe, self.game_var)
        self.dex_selector = OptionMenu(self.selection_subframe, self.dex_var)
        self.search_bar = Entry(self.selection_subframe, textvariable=self.search_var, foreground="gray")
        self.pokemon_tree = Treeview(
            self.pokemon_tree_grp,
            columns=["PokemonID", "NationalDexNo", "PokemonName"],
            displaycolumns=["NationalDexNo", "PokemonName"],
            show="headings",
            height=12

        )
        self.pokemon_tree_scrollbar: Scrollbar = Scrollbar(
            self.pokemon_tree_grp,
            orient=VERTICAL,
            command=self.pokemon_tree.yview
        )
        self.form_tree = Treeview(
            self.selection_subframe,
            columns=["PokemonID", "FormName"],
            displaycolumns=["FormName"],
            show="headings",
            height=5
        )

        # Control configurations
        self.search_bar.insert(0, "Search...")
        self.search_bar.bind("<FocusIn>", self.on_search_bar_focus_in)
        self.search_bar.bind("<FocusOut>", self.on_search_bar_focus_out)
        self.search_var.trace("w", self.on_search_var_changed)
        self.dex_var.set("Not Selected")
        self.pokemon_tree.column("NationalDexNo", width=30, minwidth=30)
        self.pokemon_tree.heading(
            "NationalDexNo",
            text="#",
            command=lambda col="NationalDexNo": sort_pokemon_by_dex_no(self.pokemon_tree, col, True)
        )
        self.pokemon_tree.heading(
            "PokemonName",
            text="Pokemon",
            command=lambda col="PokemonName": sort_pokemon_by_name(self.pokemon_tree, col, False)

        )
        self.pokemon_tree.configure(yscrollcommand=self.pokemon_tree_scrollbar.set)
        self.form_tree.column("FormName")
        self.form_tree.heading("FormName", text="Form")

        # Place controls
        self.game_selector.pack(side=TOP, fill=X)
        self.dex_selector.pack(side=TOP, fill=X)
        self.search_bar.pack(side=TOP, fill=X)
        self.pokemon_tree.pack(side=LEFT, fill=BOTH)
        self.pokemon_tree_scrollbar.pack(side=LEFT, fill=Y)
        self.pokemon_tree_grp.pack(side=TOP, fill=X)
        self.form_tree.pack(side=TOP, fill=X)

        # Place Subframe
        self.selection_subframe.pack(side=LEFT, fill=Y)

    def create_profile_subframe(self):
        # Subframe to contain controls.
        self.profile_subframe = Frame(self.viewer_frame)
        self.form_group = Frame(self.profile_subframe)
        self.type_group = Frame(self.profile_subframe)

        # Control declarations
        self.shiny_chk = Checkbutton(self.form_group, text="Shiny", variable=self.shiny)
        self.portrait_icon_lbl = Label(self.profile_subframe)
        self.primary_type_icon_lbl = Label(self.type_group)
        self.secondary_type_icon_lbl = Label(self.type_group)

        # Place controls
        self.shiny_chk.grid(column=0, row=0)
        self.form_group.pack(side=LEFT, fill=Y, expand=True)

        self.portrait_icon_lbl.pack(side=LEFT, fill=Y, expand=True)

        self.primary_type_icon_lbl.grid(column=0, row=0)
        self.secondary_type_icon_lbl.grid(column=0, row=1)
        self.type_group.pack(side=LEFT, fill=Y, expand=True)

        # Place Subframe.
        self.profile_subframe.pack(side=TOP)

    # Create subframe to hold stat-related UI elements.
    def create_stats_subframe(self):
        # Subframe to contain controls.
        self.stats_subframe = Frame(self.viewer_frame)

        # Control declarations/placement.
        labels: list = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]

        for i, label in enumerate(labels):
            # Stat names
            stat_name_label: Label = Label(self.stats_subframe, text=labels[i], width=5)
            stat_name_label.grid(column=0, row=i)

            # Stat values
            stat_value_label: Label = Label(self.stats_subframe, text=0, width=5)
            stat_value_label.grid(column=1, row=i)
            self.stat_value_labels.append(stat_value_label)

            # Stat bars
            stat_bar: Progressbar = Progressbar(
                self.stats_subframe,
                length=200,
                mode="determinate"
            )
            stat_bar.grid(column=4, row=i, pady=2, padx=(0, 10))
            self.stat_bars.append(stat_bar)

        # Place Subframe.
        self.stats_subframe.pack(side=TOP)

    def refresh_type_icons(self, type_icons: tuple):
        # Refresh primary type
        self.primary_type_icon = PhotoImage(data=type_icons[0])
        self.primary_type_icon_lbl.config(image=self.primary_type_icon)

        # Refresh secondary type
        self.secondary_type_icon = PhotoImage(data=type_icons[1])
        self.secondary_type_icon_lbl.config(image=self.secondary_type_icon)

    # Set stat bar data to passed list of stats.
    def refresh_stats(self, stats: list) -> None:
        first_quarter: int = int(self.max_stats[1] / 4)
        second_quarter: int = first_quarter * 2
        third_quarter: int = first_quarter * 3

        for i, stat_bar in enumerate(self.stat_bars):
            self.stat_value_labels[i].configure(text=stats[i])
            if i == 0:
                stat_bar.configure(
                    value=stats[i],
                    maximum=self.max_stats[0]
                )
            else:
                stat_bar.configure(
                    value=stats[i],
                    maximum=self.max_stats[1]
                )

            # Update the style based on the value
            if stats[i] < first_quarter:
                stat_bar["style"] = "red.Horizontal.TProgressbar"
            elif stats[i] < second_quarter:
                stat_bar["style"] = "yellow.Horizontal.TProgressbar"
            elif stats[i] < third_quarter:
                stat_bar["style"] = "green.Horizontal.TProgressbar"
            else:
                stat_bar["style"] = "blue.Horizontal.TProgressbar"

    def refresh_max_stats(self, max_stats: tuple) -> None:
        self.max_stats = max_stats

    def refresh_portrait_icon(self, icon_data: bytes) -> None:
        self.portrait_icon = PhotoImage(data=icon_data)
        self.portrait_icon_lbl.config(image=self.portrait_icon)

    # Search Pokémon in selector by either name or dex number.
    def search_pokemon_tree(self, term: str) -> None:
        self.pokemon_tree.delete(*self.pokemon_tree.get_children())
        for values in self.selector_data:
            if term in values[2].lower() or term == str(values[1]):
                self.pokemon_tree.insert("", END, values=values)
        focus_first(self.pokemon_tree)

    # Returns national dex ID of current selection.
    def get_national_dex_id(self) -> int:
        pokemon: str = self.pokemon_tree.focus()
        if pokemon:
            national_dex_id: int = int(self.pokemon_tree.item(pokemon)["values"][0])
        else:
            national_dex_id: int = 0
        return national_dex_id

    # Returns Pokémon ID of current selection.
    def get_pokemon_id(self) -> int:
        pokemon: str = self.form_tree.focus()
        if pokemon:
            pokemon_id: int = int(self.form_tree.item(pokemon)["values"][0])
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

    # Flushes Pokémon values, and replaces them with the passed Pokémon data.
    def refresh_pokemon_tree(self, pokemon: list) -> None:
        # Store passed data
        self.selector_data = pokemon

        # Delete items from tree
        self.pokemon_tree.delete(*self.pokemon_tree.get_children())

        # Populate Tree
        for values in self.selector_data:
            self.pokemon_tree.insert("", END, values=values)

        self.on_search_var_changed()
        focus_first(self.pokemon_tree)

    # Flushes form values, and replaces them with the passed Pokémon form data.
    def refresh_form_tree(self, forms: list) -> None:
        # Delete items from tree
        self.form_tree.delete(*self.form_tree.get_children())

        # Populate Tree
        for form in forms:
            if form[1]:
                self.form_tree.insert("", END, values=form)
            else:
                self.form_tree.insert("", END, values=(form[0], "Default"))
        focus_first(self.form_tree)

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
        else:
            self.dex_var.set("None")

    # Event handlers
    def on_search_var_changed(self, *args):
        term: str = self.search_var.get().lower()
        if term != "search...":
            self.search_pokemon_tree(term)

    def on_search_bar_focus_in(self, event):
        if self.search_bar.get() == "Search...":
            self.search_bar.delete(0, END)
            self.search_bar.config(foreground="black")

    def on_search_bar_focus_out(self, event):
        if self.search_bar.get() == "":
            self.search_bar.insert(0, "Search...")
            self.search_bar.config(foreground="gray")
