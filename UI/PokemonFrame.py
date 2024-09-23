from tkinter import END, EW, NS, StringVar, VERTICAL
from tkinter.ttk import Entry, Frame, Treeview, Scrollbar


# Class to extend Tkinter Frame's functionality
# UI element to display a list of Pokémon
class PokemonFrame:
    def __init__(self, root) -> None:
        self.pokemon_frame = Frame(root)

        # For storing passed Pokémon data
        self.selector_data: list = []

        # UI declarations
        self.selector = Treeview(self.pokemon_frame)
        self.selector_scrollbar = Scrollbar(self.pokemon_frame)
        self.search_var = StringVar()
        self.search_bar = Entry(self.pokemon_frame, textvariable=self.search_var)

        # Configure UI controls
        self._build_search_bar()
        self._build_selector()

    # Focus first item in selector
    def focus_first(self) -> None:
        self.selector.focus_set()
        children: tuple = self.selector.get_children()
        if children:
            self.selector.focus(children[0])
            self.selector.selection_set(children[0])

    # Flushes selector values, and replaces them with the passed Pokémon data.
    def refresh_pokemon(self, pokemon: list) -> None:
        # Store passed data
        self.selector_data = pokemon

        # Delete items from tree
        self.selector.delete(*self.selector.get_children())

        # Populate Tree
        for values in self.selector_data:
            self.selector.insert("", END, values=values)

        self._on_search_var_changed()
        self.focus_first()

    # Search Pokémon in selector by either name or dex number.
    def search_pokemon(self, term: str):
        for item in self.selector.get_children():
            self.selector.delete(item)
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

    # Place frame in grid; to be called from main function
    def to_grid(self, col: int, row: int) -> None:
        self.pokemon_frame.grid(column=col, row=row)

    # Build TK controls within frame.
    def _build_search_bar(self) -> None:
        self.search_var.trace("w", self._on_search_var_changed)
        self.search_bar.grid(column=0, row=0, columnspan=2, sticky=EW)

    # Build Pokémon selector (TreeView) plus scrollbar within frame.
    def _build_selector(self):
        # Configure selector
        self.selector.config(columns=["PokemonID", "NationalDexNo", "PokemonName"],
                             displaycolumns=["NationalDexNo", "PokemonName"],
                             show="headings",
                             yscrollcommand=self.selector_scrollbar.set)
        self.selector.column("NationalDexNo", width=30, minwidth=30)
        self.selector.heading("NationalDexNo", text="#")
        self.selector.heading("PokemonName", text="Pokemon")

        # Configure scrollbar
        self.selector_scrollbar.config(orient=VERTICAL, command=self.selector.yview)

        # Place controls
        self.selector.grid(column=0, row=1, rowspan=2)
        self.selector_scrollbar.grid(column=1, row=1, rowspan=2, sticky=NS)

    # Event handlers
    def _on_search_var_changed(self, *args):
        term: str = self.search_var.get().lower()
        self.search_pokemon(term)


# Main function for debugging purposes
def main() -> None:
    from tkinter import Tk
    root = Tk()
    pf = PokemonFrame(root)
    pf.refresh_pokemon([(0, 1, "TestPokemon1"), (1, 2, "TestPokemon2")])
    pf.to_grid(0, 0)
    root.mainloop()


if __name__ == "__main__":
    main()
