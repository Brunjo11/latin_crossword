import random
import json
import numpy as np

# Carica parole e indizi
with open("words.json", "r") as f:
    words_data = json.load(f)

words = [w["word"] for w in words_data]
clues = [w["clue"] for w in words_data]

# Dimensione griglia
GRID_SIZE = 15
grid = np.full((GRID_SIZE, GRID_SIZE), " ")

def can_place(word, row, col, direction):
    if direction == "H":
        if col + len(word) > GRID_SIZE:
            return False
        for i, c in enumerate(word):
            if grid[row, col+i] != " " and grid[row, col+i] != c:
                return False
    else:  # verticale
        if row + len(word) > GRID_SIZE:
            return False
        for i, c in enumerate(word):
            if grid[row+i, col] != " " and grid[row+i, col] != c:
                return False
    return True

def place_word(word):
    directions = ["H", "V"]
    random.shuffle(directions)
    for direction in directions:
        for _ in range(100):
            row = random.randint(0, GRID_SIZE-1)
            col = random.randint(0, GRID_SIZE-1)
            if can_place(word, row, col, direction):
                for i, c in enumerate(word):
                    if direction == "H":
                        grid[row, col+i] = c
                    else:
                        grid[row+i, col] = c
                return True
    return False

# Posiziona tutte le parole
for word in words:
    if not place_word(word):
        print(f"Non sono riuscito a inserire la parola: {word}")

# Stampa griglia
print("\nCRUCIVERBA:")
for row in grid:
    print(" ".join(row))

# Stampa indizi
print("\nINDIZI:")
for i, clue in enumerate(clues):
    print(f"{i+1}. {clue}")
