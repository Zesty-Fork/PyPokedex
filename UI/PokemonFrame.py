from tkinter import END
from tkinter.ttk import Frame, Treeview


# Class to extend Tkinter Frame's functionality
# UI element to display a list of Pokemon
class PokemonFrame:
    def __init__(self, root):
        self.pokemon_frame = Frame(root)
        self.selector = None

        self._set_pokemon_controls()

    # Place frame in grid; to be called from main function
    def frame_grid(self, col: int, row: int):
        self.pokemon_frame.grid(column=col, row=row)

    def _set_pokemon_controls(self):
        self.selector = Treeview(
            self.pokemon_frame,
            columns=["PokemonID", "NationalDexNo", "PokemonName"],
            displaycolumns=["NationalDexNo", "PokemonName"],
            show="headings")

        self.selector.column("NationalDexNo", width=30, minwidth=30)
        self.selector.heading("NationalDexNo", text="#")
        self.selector.heading("PokemonName", text="Pokemon")
        self.selector.grid(column=0, row=0, rowspan=2)

    def focus_first(self) -> None:
        # Focus first item
        self.selector.focus_set()
        children: tuple = self.selector.get_children()
        if children:
            self.selector.focus(children[0])
            self.selector.selection_set(children[0])

    def refresh_pokemon(self, pokemon: list) -> None:
        # Delete items from tree
        self.selector.delete(*self.selector.get_children())

        # Populate Tree
        for values in pokemon:
            self.selector.insert("", END, values=values)

        self.focus_first()

    def get_pokemon_id(self) -> int:
        pokemon = self.selector.focus()
        if pokemon:
            pokemon_id: int = self.selector.item(pokemon)["values"][0]
        else:
            pokemon_id: int = 0
        return pokemon_id


# Main function for debugging purposes
def main() -> None:
    from tkinter import Tk
    root = Tk()
    pf = PokemonFrame(root)
    pf.refresh_pokemon([(0, 1, "TestPokemon")])
    pf.frame_grid(0, 0)
    root.mainloop()


if __name__ == "__main__":
    main()
