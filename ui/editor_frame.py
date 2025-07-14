# Python Libraries
import tkinter as tk
from tkinter.ttk import Frame, Treeview
from tkinter.filedialog import askopenfilename

# Local Libraries
from db.db import PokedexDB


def image_to_blob(image_path: str) -> bytes:
    blob: bytes = b""
    with open(image_path, "rb") as image_file:
        blob = image_file.read()
    return blob


class EditorFrame(Frame):
    def __init__(self):
        # Database
        super().__init__()
        self.db: PokedexDB = PokedexDB()

        # Selection Variables
        self.cur_pokemon_id: int = 1

        # Control Variables
        self.pkmn_tree = None
        self.icon_normal_lbl = None
        self.icon_shiny_lbl = None

        self._create_main_window()

    def _create_main_window(self):
        columns: list = ["PokemonID", "NationalDexNo", "PokemonName"]
        displaycolumns: list = ["NationalDexNo", "PokemonName"]
        self.pkmn_tree = Treeview(self, columns=columns, displaycolumns=displaycolumns, show="headings")
        self.pkmn_tree.column("NationalDexNo", width=30, minwidth=30)

        # Define headings
        self.pkmn_tree.heading("NationalDexNo", text="#")
        self.pkmn_tree.heading("PokemonName", text="Pokemon")

        # Control variable declarations
        self.pkmn_tree.bind("<<TreeviewSelect>>", self._on_pokemon_selected)
        self.icon_normal_lbl = tk.Label(self, width=112, height=112)
        self.icon_shiny_lbl = tk.Label(self, width=112, height=112)
        self.split_genders_btn = tk.Button(self, text="Split Gendered Forms", command=self._on_split_genders_clicked)
        self.add_gigantamax_btn = tk.Button(self, text="Add Gigantamax Form", command=self._on_gigantamax_clicked)

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

    def _refresh_pokemon_list(self) -> None:
        # Delete items from tree
        self.pkmn_tree.delete(*self.pkmn_tree.get_children())

        # Populate Tree
        for pokemon in self.db.get_pokemon("1", "1"):
            self.pkmn_tree.insert("", tk.END, values=pokemon)

    # Event Handlers
    def _on_pokemon_selected(self, event):
        selected_pokemon = self.pkmn_tree.focus()
        self.cur_pokemon_id = self.pkmn_tree.item(selected_pokemon)["values"][0]

        icon_normal_data: bytes = self.db.get_portrait_icon(self.cur_pokemon_id, False)
        if icon_normal_data:
            self.icon_normal = tk.PhotoImage(data=icon_normal_data)
            self.icon_normal_lbl.config(image=self.icon_normal, width=112, height=112)
        else:
            self.icon_normal = tk.PhotoImage(file="Placeholder.png")
            self.icon_normal_lbl.config(image=self.icon_normal, width=112, height=112)

        icon_shiny_data: bytes = self.db.get_portrait_icon(self.cur_pokemon_id, True)
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
            self.db.update_portrait_icon(image_blob, self.cur_pokemon_id, False)
            self._on_pokemon_selected("event")

    def _on_icon_shiny_clicked(self, event) -> None:
        filename: str = tk.filedialog.askopenfilename()
        if filename:
            image_blob: bytes = image_to_blob(filename)
            self.db.update_portrait_icon(image_blob, self.cur_pokemon_id, True)
            self._on_pokemon_selected("event")

    def _on_split_genders_clicked(self) -> None:
        # self.db.split_gender_forms(self.cur_pokemon_id)
        self._refresh_pokemon_list()

    def _on_gigantamax_clicked(self):
        # self.db.add_gigantamax_form(self.cur_pokemon_id)
        self._refresh_pokemon_list()
