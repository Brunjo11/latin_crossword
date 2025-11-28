import streamlit as st
import json

st.set_page_config(page_title="Cruciverba Latino", layout="wide")
st.title("🧩 Cruciverba di Locuzioni Latine")

# Load words
with open("words.json", "r", encoding="utf-8") as f:
    words_list = json.load(f)["words"]

# Determine grid size
max_row = max(word["row"] + (len(word["word"]) if word["direction"] == "V" else 1) for word in words_list)
max_col = max(word["col"] + (len(word["word"]) if word["direction"] == "H" else 1) for word in words_list)

# Initialize grid state
if "grid" not in st.session_state:
    st.session_state.grid = [["" for _ in range(max_col)] for _ in range(max_row)]

# Fill grid numbers for clues
numbering = {}
for idx, word in enumerate(words_list, 1):
    r, c = word["row"], word["col"]
    if (r, c) not in numbering:
        numbering[(r, c)] = str(idx)
    word["number"] = str(idx)

# Sidebar clues
st.sidebar.header("📜 Definizioni")
st.sidebar.subheader("Orizzontali")
for w in words_list:
    if w["direction"] == "H":
        st.sidebar.write(f"{w['number']} → {w['clue']}")
st.sidebar.subheader("Verticali")
for w in words_list:
    if w["direction"] == "V":
        st.sidebar.write(f"{w['number']} → {w['clue']}")

# Draw grid
st.header("🧩 Griglia")
for r in range(max_row):
    cols = st.columns(max_col)
    for c in range(max_col):
        key = f"{r}_{c}"
        val = st.session_state.grid[r][c]
        display = val if val else ""
        # Show number if this is start of a word
        num_label = numbering.get((r, c), "")
        if num_label:
            display = num_label
        st.session_state.grid[r][c] = cols[c].text_input("", value=val, max_chars=1, key=key)

# Check button
if st.button("✔️ Controlla"):
    correct = True
    for w in words_list:
        r, c = w["row"], w["col"]
        for i, letter in enumerate(w["word"].upper()):
            rr, cc = (r + i, c) if w["direction"] == "V" else (r, c + i)
            user_letter = st.session_state.grid[rr][cc].upper()
            if user_letter != letter:
                correct = False
                break
    if correct:
        st.success("🎉 Complimenti! Tutte le parole sono corrette.")
    else:
        st.error("❌ Alcune lettere sono sbagliate. Riprova!")

# Reset
if st.button("🔄 Reset"):
    for r in range(max_row):
        for c in range(max_col):
            st.session_state.grid[r][c] = ""
    st.experimental_rerun()
