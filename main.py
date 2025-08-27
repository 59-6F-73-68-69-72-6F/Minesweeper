"""
Minesweeper Game
This script implements a command-line Minesweeper game.
Players can discover squares, flag potential mine locations, and unflag squares.
The game ends when all non-mine squares are revealed (win) or a mine is hit (lose).
"""

import os
import random
import string
import time
from pprint import pprint

SQUARE, MINE, FLAG, OK, BOOM = "⬛", "💣", "🚩", "✅", "💥"
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
AREA = 13
choice = 0
mines_amount, flags_amount = 18, 18
layout = []
answer_layout = []
loose = False


ART = r"""
 __ __ _ __  _ ___  __  _   _  ___ ___ ___ ___ ___ 
|  V  | |  \| | __/' _/| | | || __| __| _,\ __| _ \
| \_/ | | | ' | _|`._`.| 'V' || _|| _|| v_/ _|| v /
|_| |_|_|_|\__|___|___/!_/ \_!|___|___|_| |___|_|_\
"""


# FUNCTIONS -------------------
def create_layout(area: int) -> list:
    """
    Creates the initial 'game layout' and 'answer layout'.
    """
    global layout, answer_layout
    title_row = string.ascii_uppercase[:area]
    for row in range(area):
        layout.append([])
        answer_layout.append([])
        for column in range(area):
            if column == 0:
                layout[row].append(title_row[row])
                answer_layout[row].append(title_row[row])
                continue
            layout[row].append(SQUARE)
            answer_layout[row].append(SQUARE)
    return layout, answer_layout


def scatter_mines(mines: int, layout: list) -> list:
    """
    Randomly scatters mines across the 'answer layout'.
    """
    placed_mines = 0
    while placed_mines < mines:
        x = random.randint(0, len(layout) - 1)
        y = random.randint(1, len(layout[0]) - 1)
        if answer_layout[x][y] == SQUARE:
            answer_layout[x][y] = MINE
            placed_mines += 1
    return answer_layout


def flood_fill(x: int, y: int):
    """
    Recursively reveals squares in the given layout.
    If a square has no adjacent mines, it reveals all adjacent squares.
    """
    if x < 0 or x >= AREA or y < 1 or y >= AREA or layout[x][y] != SQUARE:
        return

    count_mine = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if 0 <= i < AREA and 1 <= j < AREA and answer_layout[i][j] == MINE:
                count_mine += 1

    if count_mine > 0:
        layout[x][y] = " " + str(count_mine)
        answer_layout[x][y] = " " + str(count_mine)
    else:
        layout[x][y] = "  "
        answer_layout[x][y] = "  "
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i != x or j != y:
                    flood_fill(i, j)


def core_mechanic(layout: list, answer_layout: list, coordinate: str) -> list:
    """
    Handles the core game mechanics based on user input.
    Allows discovering squares, placing flags, and unflagging squares.
    Updates the game layout and checks for win/loss conditions.
    """
    global choice, flags_amount, loose
    try:
        x = string.ascii_uppercase.index(coordinate[0])
        y = int(coordinate[1:])
    except ValueError as e:
        print(RED + "Please enter a valid coordinate."+RESET)
        time.sleep(1.5)
        return layout
    # COORDINATE VALIDATION - ERROR HANDLE
    if x < 0 or x >= AREA or y < 1 or y >= len(layout[0]):
        print(RED + "Coordinates out of bounds. Please try again." + RESET)
        time.sleep(1.5)
        return layout

    if choice == 1 and answer_layout[x][y] == SQUARE:
        try:
            flood_fill(x, y)
            return layout
        except IndexError as e:
            print(e)

    elif choice == 1 and layout[x][y] == FLAG or choice == 2 and layout[x][y] == FLAG:
        return layout

    elif choice == 1 and layout[x][y] == FLAG and answer_layout[x][y] == MINE:
        return layout

    elif choice == 1 and answer_layout[x][y] == MINE:
        layout[x][y] = BOOM
        answer_layout[x][y] = BOOM
        loose = True
        print(RED + "+++++++++++++++++++++++ YOU LOSE +++++++++++++++++++++++" + RESET)
        return layout, loose

    elif choice == 2 and layout[x][y] == SQUARE:
        if flags_amount > 0:
            layout[x][y] = FLAG
            flags_amount -= 1
        else:
            print(RED + "No flags left!" + RESET)
            time.sleep(1.5)
        return layout

    elif choice == 3 and layout[x][y] == FLAG:
        layout[x][y] = SQUARE
        flags_amount += 1
        return layout

    elif choice == 3 and layout[x][y] == SQUARE:
        return layout


def victory_checker(layout: list) -> bool:
    """
    Checks if the player has won the game by revealing all non-mine squares.
    """
    revealed_squares = 0
    for x in range(AREA):
        for y in range(1, AREA):
            if layout[x][y] != SQUARE and layout[x][y] != FLAG:
                revealed_squares += 1
    if revealed_squares == (AREA * (AREA - 1)) - mines_amount:
        print(GREEN + "+++++++++++++++++++++++ YOU WIN +++++++++++++++++++++++" + RESET)
        return True
    return False


def show_result(layout: list, answer_layout: list) -> list:
    """
    Compares the player's flags with the actual mine locations.
    Updates the answer_layout to show correctly placed flags and
    incorrectly placed flags.
    """
    for x in range(AREA):
        for y in range(AREA):
            if layout[x][y] == FLAG and answer_layout[x][y] != MINE:
                answer_layout[x][y] = FLAG
            elif layout[x][y] == FLAG and answer_layout[x][y] == MINE:
                answer_layout[x][y] = OK
    return answer_layout


# -------------------------- MAIN --------------------------
os.system('clear')  # 'cls' for windows
print(f"{RED} {ART} {RESET}\n")
create_layout(AREA)
scatter_mines(mines_amount, answer_layout)
title = []
for n in range(AREA):
    if n == 0:
        title.append("😐")
    elif n < 10:
        title.append(" " + str(n))
    else:
        title.append(str(n))
print(RED)
print(title, RESET)
pprint(layout)
print(f"{YELLOW}flags amount:{RESET} {flags_amount}")

#  MAIN LOOP
while victory_checker(layout) is False or loose is False:
    coord = input(GREEN + "Enter your coordinate: " + RESET).upper()
    try:
        choice = int(input(GREEN + "Enter your choice, 1)Discover  -  2)Flag  -  3)Unflag ," +
                           YELLOW + "Type 1 or 2 or 3:  " + RESET))
    except ValueError as e:
        print(RED + "Please enter a number, between 1 and 3." + RESET)
        time.sleep(1.5)
        continue
    core_mechanic(layout, answer_layout, coord)
    if victory_checker(layout) is True or loose is True:
        if loose:
            title[0] = "😵"
        else:
            title[0] = "🤩"
        break

    os.system('clear')  # 'cls' for windows
    print(f"{RED} {ART} {RESET}\n")
    print(RED)
    print(title, RESET)
    pprint(layout)
    print(f"{YELLOW}flags amount:{RESET} {flags_amount}")

show_result(layout, answer_layout)
print(RED)
print(title, RESET)
pprint(answer_layout)
