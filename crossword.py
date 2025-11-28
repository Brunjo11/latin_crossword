import streamlit as st
import json

# Load words and clues
with open('words.json', 'r') as f:
    data = json.load(f)

clues = data['clues']
solution = data['solution']  # A dictionary with keys as cell positions and values as letters

# Initialize session state
if 'grid' not in st.session_state:
    st.session_state.grid = {cell: "" for cell in solution.keys()}

st.title("🧩 Cruciverba Interattivo")
st.write("Compila il cruciverba e premi **Controlla** per verificare le risposte. Usa **Reset** per ricominciare.")

# Display clues
st.header("📜 Definizioni")
for key, text in clues.items():
    st.write(f"**{key}** – {text}")

# Crossword grid UI
st.header("🧩 Griglia del Cruciverba")
cols = sorted({int(pos.split(',')[1]) for pos in solution.keys()})
rows = sorted({int(pos.split(',')[0]) for pos in solution.keys()})

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

# Check button
if st.button("✔️ Controlla"):
    correct = True
    for cell, correct_letter in solution.items():
        if st.session_state.grid[cell].upper() != correct_letter.upper():
            correct = False
    if correct:
        st.success("🎉 Complimenti! Hai completato il cruciverba correttamente!")
    else:
        st.error("❌ Alcune risposte sono sbagliate. Riprova!")

# Reset button
if st.button("🔄 Reset"):
    for cell in st.session_state.grid:
        st.session_state.grid[cell] = ""
    st.experimental_rerun()
    
