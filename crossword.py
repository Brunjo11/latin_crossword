import streamlit as st
import random
import json
import numpy as np

# Titolo
st.title("Cruciverba Latino")

# Carica parole e indizi
@st.cache_data
def load_words():
    with open("words.json", "r") as f:
        return json.load(f)

words_data = load_words()
words = [w["word"] for w in words_data]
clues = [w["clue"] for w in words_data]

# Dimensione griglia
GRID_SIZE = 15

def can_place(grid, word, row, col, direction):
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

def place_word(grid, word):
    directions = ["H", "V"]
    random.shuffle(directions)
    for direction in directions:
        for _ in range(100):
            row = random.randint(0, GRID_SIZE-1)
            col = random.randint(0, GRID_SIZE-1)
            if can_place(grid, word, row, col, direction):
                for i, c in enumerate(word):
                    if direction == "H":
                        grid[row, col+i] = c
                    else:
                        grid[row+i, col] = c
                return True
    return False

def generate_crossword():
    grid = np.full((GRID_SIZE, GRID_SIZE), " ")
    for word in words:
        place_word(grid, word)
    return grid

# Bottone per generare cruciverba
if st.button("Genera Cruciverba"):
    grid = generate_crossword()
    # Mostra griglia
    st.subheader("Griglia")
    st.text("\n".join([" ".join(row) for row in grid]))
    # Mostra indizi
    st.subheader("Indizi")
    for i, clue in enumerate(clues):
        st.write(f"{i+1}. {clue}")
