# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="debating-agents", layout="wide")
st.title("Debate Simulation")

topic = st.text_input("Enter debate topic:", )

if st.button("Start Debate"):
    response = requests.get(f"http://127.0.0.1:8000/start_debate?topic={topic}")
    debate_messages = response.json()["messages"]

    for msg in debate_messages:
        st.write(msg)
