import streamlit as st
import json

# Load words and clues
with open('words.json', 'r') as f:
    data = json.load(f)

clues = data['clues']            # { "1-Orizzontale": "definizione" ... }
solutions_words = data['words']   # { "1-Orizzontale": "CARPEDIEM", ... }
solution = data['solution']       # { "0,0": "C", ... }

# Initialize session state
if 'user_words' not in st.session_state:
    st.session_state.user_words = {key: "" for key in clues.keys()}

if 'grid' not in st.session_state:
    st.session_state.grid = {cell: "" for cell in solution.keys()}

st.title("🧩 Cruciverba Interattivo – Inserimento Parole Intere")
st.write("Inserisci la parola per ogni definizione. Verrà riempita automaticamente nella griglia.")

# --- PAROLE (input interi) ---
st.header("✏️ Inserisci le parole intere dalle definizioni")
for key, definition in clues.items():
    st.session_state.user_words[key] = st.text_input(
        f"{key} – {definition}",
        st.session_state.user_words[key]
    )

# --- AUTORIEMPIMENTO GRIGLIA ---
st.header("🧩 Griglia del Cruciverba (auto-riempita)")
cols = sorted({int(pos.split(',')[1]) for pos in solution.keys()})
rows = sorted({int(pos.split(',')[0]) for pos in solution.keys()})

# Fill the grid from word inputs
if st.button("📥 Riempie la griglia"):
    for clue_key, word in st.session_state.user_words.items():
        if clue_key in solutions_words:
            correct_word = solutions_words[clue_key]
            for idx, letter in enumerate(word.upper()):
                if idx < len(correct_word):
                    # fill only valid letters
                    # locate all cells of this word
                    positions = [cell for cell, sol_letter in solution.items()
                                 if sol_letter == correct_word[idx]]
            # NOTE: actual mapping from clue -> positions should be in words.json
    st.warning("⚠️ Il riempimento completo richiede la mappa delle posizioni per ogni parola.")

# --- VISUALIZZAZIONE GRIGLIA ---
grid_table = []
for r in rows:
    row_cells = []
    for c in cols:
        cell_key = f"{r},{c}"
        if cell_key in solution:
            row_cells.append(st.text_input("", st.session_state.grid[cell_key], key=cell_key, max_chars=1))
        else:
            row_cells.append(" ")
    grid_table.append(row_cells)

# --- VERIFICA ---
if st.button("✔️ Controlla"):
    correct = True
    for cell, correct_letter in solution.items():
        if st.session_state.grid[cell].upper() != correct_letter.upper():
            correct = False
    if correct:
        st.success("🎉 Complimenti! Tutto corretto!")
    else:
        st.error("❌ Ci sono errori nella griglia.")

# --- RESET ---
if st.button("🔄 Reset totale"):
    for k in st.session_state.user_words:
        st.session_state.user_words[k] = ""
    for k in st.session_state.grid:
        st.session_state.grid[k] = ""
    st.experimental_rerun()
