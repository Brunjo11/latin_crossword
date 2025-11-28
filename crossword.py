import json
import streamlit as st

st.set_page_config(page_title="Cruciverba Latino", page_icon="✒️", layout="centered")

st.title("📘 Cruciverba di Locuzioni Latine")
st.write("Scegli una definizione e prova a indovinare la parola latina corretta!")

# --- Load words.json ---
try:
    with open("words.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        words_list = data.get("words", [])
except Exception as e:
    st.error("❌ Errore nel caricamento di words.json:")
    st.code(str(e))
    st.stop()

if not words_list:
    st.error("❌ words.json è vuoto o formattato male.")
    st.stop()

# List clues
clues = {item["clue"]: item["word"] for item in words_list}

selected_clue = st.selectbox("📌 Scegli una definizione:", list(clues.keys()))

user_answer = st.text_input("✏️ La tua risposta (solo lettere, senza spazi):")

if st.button("Verifica"):
    correct_answer = clues[selected_clue].upper().replace(" ", "")
    user_clean = user_answer.upper().replace(" ", "")

    if user_clean == correct_answer:
        st.success("✅ Corretto!")
    else:
        st.error(f"❌ Errato! La risposta corretta era **{correct_answer}**.")
