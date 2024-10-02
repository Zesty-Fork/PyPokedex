# PyPokedex
Pokédex written in Python.

## Overview
- This is a straightforward Python Pokédex application designed to provide game-accurate information about Pokémon from Generation 1 through Generation 9. The app uses a SQLite backend to store all data, including images. It also features a Tkinter-based frontend. Notably, the application has no pythonic dependencies and runs on Python 3.8+.

## Features
- **View Pokémon Data**: View Pokémon images (both shiny and normal), abilities, stats, types, and forms.
- **Filter by Game/Pokédex**: Filter data by Game/Pokédex to accurately view all current and historic Pokémon records.
- **Search Functionality**: Easily find specific Pokémon using the search feature.
- **Accurate Data**: All data is vetted and accurate to the original game releases, accounting for changes in abilities, stats and types between games.

## Requirements
- Python 3.8 (or newer)

## Installation
- No installation is required.

## Usage
1. **Launch the Application**: Run the `PyPokedex.py` file to start the application.
   ```bash
   python PyPokedex.py

## Planned Changes/Features
1. **Pokédex Editor**: Quickly edit or add new Pokémon data through the GUI frontend.
2. **Further Data Vetting** While the database is accurate, it is not perfect, and there are still some areas for cleanup.
3. **Executable** Compile the Python app into executables for easy, nontechnical usage.
4. **Add Legends: Z-A data** Upon release, new data should be captured ASAP into the SQLite database.
5. **Java Version** Create a Java version of the application.