# Python Libraries
from tkinter import Tk, ttk, StringVar, TclError, W, N

# Global Declarations
TITLE: str = "PyPokedex"
VERSION: str = "1.0.0"  # TODO move to attributes file of some kind


def create_pokemon_viewer_frame(window):
    frame = ttk.Frame(window)

    frame.columnconfigure(0, weight=1)
    search_bar = ttk.Entry(frame)
    pokemon_list = ttk.Treeview(frame)

    search_bar.grid(column=0, row=0, sticky=W)
    pokemon_list.grid(column=0, row=1, sticky=W)

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame


# Local Libraries
def create_main_window():
    root = Tk()
    root.title(TITLE)
    root.resizable(False, False)

    # Windows OS only (remove the minimize/maximize button)
    try:
        root.attributes("-toolwindow", True)
    except TclError:
        print("Not supported on your platform")

    # layout on the root window

    frame1 = create_pokemon_viewer_frame(root)
    frame2 = create_pokemon_viewer_frame(root)
    frame3 = create_pokemon_viewer_frame(root)
    frame4 = create_pokemon_viewer_frame(root)

    frame1.grid(column=0, row=0, rowspan=2)
    frame2.grid(column=1, row=0)
    frame3.grid(column=2, row=0)
    frame4.grid(column=2, row=1)

    root.mainloop()


def main():
    create_main_window()


if __name__ == "__main__":
    main()
