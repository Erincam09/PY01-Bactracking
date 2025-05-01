# Maze Game in Python using Tkinter

A two-mode maze game (Classic and Free) with graphical interface, player movement, and save/load features.

---

## 🧩 Overview
This project is a maze-solving game built with Python and Tkinter. It allows users to:
- Play in Classic Mode, where the maze is automatically solved using backtracking.
- Play in Free Mode, where the player moves manually using arrow keys.
- Generate random mazes.
- Save and load game sessions.

---

## 🧪 Requirements
- Python 3.x
- `tkinter` (included by default in most Python installations)
- `Pillow` for image processing

To install Pillow:
```bash
pip install pillow
```

---

## 🚀 How to Run the Game
1. Download the `Laberinto.py` file and the `Partidas.json` file into the same folder.
2. Ensure you have the image `pic/fondo_menu.png` if you want the menu background to load.
3. Run the game with:
```bash
python Laberinto.py
```
4. The main menu will open. Choose:
   - Classic Mode
   - Free Mode
   - Load Game

---

## 🕹️ Game Modes
### Classic Mode
- Select a starting point with a click.
- Press "Solve Maze" to find all paths from start to finish.
- Browse the shortest, longest, and most optimal paths.

### Free Mode
- The player is placed in a random walkable cell.
- Move using arrow keys (↑ ↓ ← →).
- Reach the finish manually.
- Optionally, use "Resolution" to see the path visualized step by step.

---

## 💾 Saving and Loading Games
- Use the "Guardar Partida" button to save your maze and progress.
- Saved games are stored in `Partidas.json`.
- From the main menu, click "Cargar Juego" to choose and load a saved game.

---

## 🧠 Algorithm Used
### Backtracking
This recursive algorithm explores all valid paths from the starting point to the finish:
- Returns every complete solution.
- Identifies:
  - Shortest path
  - Longest path
  - Path with the fewest direction changes (optimal)

Paths are drawn over the maze in green, yellow, or orange depending on type.

---

## 🗂️ Project Structure
```
Laberinto.py         → Main logic and GUI
Partidas.json        → Save file with all saved mazes
pic/fondo_menu.png   → Background image for menu 
```

---

## 👤 Author
Developed by 
    Erin Camacho
    Ginger Rodriguez 2022035672

---

## ✅ Project Status
- Classic Mode: ✅ Fully functional
- Free Mode: ✅ Fully functional


