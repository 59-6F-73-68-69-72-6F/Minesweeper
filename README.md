# Minesweeper

This is a classic command-line implementation of the Minesweeper game written in Python.

## How to Play

1.  Run the `main.py` file in your terminal:
    ```bash
    python main.py
    ```
2.  The game board will be displayed.
3.  Enter a coordinate to interact with the board (e.g., `A5`).
4.  Choose an action:
    *   **1) Discover:** Reveal a square. If you hit a mine, you lose!
    *   **2) Flag:** Place a flag on a square you suspect is a mine.
    *   **3) Unflag:** Remove a flag from a square.

## Features

*   **Classic Minesweeper Gameplay:** The timeless game of logic and deduction.
*   **Command-Line Interface:** A retro-style gaming experience.
*   **Color-Coded Output:** Easy-to-read game board with colors to highlight flags, mines, and numbers.
*   **Win/Loss Conditions:** The game ends when you reveal all non-mine squares or hit a mine.

## Game Controls

*   **Coordinates:** Enter coordinates as a letter followed by a number (e.g., `A1`, `B12`).
*   **Actions:**
    *   `1`: Discover a square.
    *   `2`: Place a flag.
    *   `3`: Remove a flag.
