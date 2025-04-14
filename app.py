
import streamlit as st
import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Chatscope", layout="wide")
st.title("Chatscope")
st.subheader("Tu año en mensajes, revelado.")

uploaded_file = st.file_uploader("Sube tu archivo de chat de WhatsApp (.txt)", type=["txt"])

def clean_message(line):
    parts = re.split(r'\] ', line, maxsplit=1)
    if len(parts) > 1:
        message = parts[1]
        return message
    return None

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()

    messages_ceaser = []
    messages_other = []
    words = []
    emojis = []
    dates = []

    for line in lines:
        match = re.match(r"\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+\d{1,2}:\d{2}.*?\] (.*?): (.*)", line)
        if match:
            date, sender, message = match.groups()
            dates.append(date)
            if "Ceaser" in sender:
                messages_ceaser.append(message)
            else:
                messages_other.append(message)
            words.extend(re.findall(r"\w+", message.lower()))
            emojis.extend(re.findall(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]+", message))

    st.markdown("### Resumen de actividad")
    col1, col2 = st.columns(2)
    col1.metric("Mensajes enviados (Ceaser)", len(messages_ceaser))
    col2.metric("Mensajes recibidos", len(messages_other))

    st.markdown("### Palabras más usadas")
    common_words = Counter(words).most_common(10)
    words_df = pd.DataFrame(common_words, columns=["Palabra", "Frecuencia"])
    st.bar_chart(words_df.set_index("Palabra"))

    st.markdown("### Emojis más usados")
    common_emojis = Counter(emojis).most_common(10)
    emoji_df = pd.DataFrame(common_emojis, columns=["Emoji", "Frecuencia"])
    st.dataframe(emoji_df)
