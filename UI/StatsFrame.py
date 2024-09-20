from tkinter.ttk import Frame, Label, Progressbar


# Class to extend Tkinter Frame's functionality
# UI element to display Pokémon stats
class StatsFrame:
    def __init__(self, root) -> None:
        self.stats_frame = Frame(root)
        self.stat_bars: list = []
        self.stat_labels: list = []

        self._build_stat_labels()
        self._build_stat_bars()

    # Set stat bar data to passed list of stats.
    def refresh_stats(self, stats: list) -> None:
        i: int = 0
        while i < 6:
            self.stat_bars[i]["value"] = stats[i]
            i += 1

    # Place frame in grid; to be called from main function
    def to_grid(self, col: int, row: int):
        self.stats_frame.grid(column=col, row=row)

    # Build stat label tk objects
    def _build_stat_labels(self) -> None:
        i: int = 0
        labels: list = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
        while i < 6:
            stat_label = Label(self.stats_frame, text=labels[i])
            stat_label.grid(column=0, row=i)
            self.stat_labels.append(stat_label)
            i += 1

    # Build stat bar tk objects
    def _build_stat_bars(self) -> None:
        i: int = 0
        while i < 6:
            stat_bar = Progressbar(self.stats_frame, style="TProgressbar", length=200, mode='determinate')
            stat_bar.grid(column=1, row=i)
            self.stat_bars.append(stat_bar)
            i += 1


# Main function for debugging purposes
def main() -> None:
    from tkinter import Tk
    root = Tk()
    sf = StatsFrame(root)
    sf.refresh_stats([10, 15, 20, 40, 30, 5])
    sf.to_grid(0, 0)
    root.mainloop()


if __name__ == "__main__":
    main()
