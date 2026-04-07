"""
Interface visuelle : chat Streamlit branché sur agent.py.
Lancement : streamlit run dashboard.py
"""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from agent import MODEL_NAME, new_user_message, reply

load_dotenv()

st.set_page_config(
    page_title="TrustHariz — Assistant",
    page_icon="💬",
    layout="centered",
)

st.title("Assistant TrustHariz")
st.caption(f"Modèle : **{MODEL_NAME}** (rapide et économique)")

if not os.getenv("OPENAI_API_KEY", "").strip():
    st.error(
        "La clé API OpenAI est absente. Créez un fichier **.env** dans ce dossier avec :\n\n"
        "`OPENAI_API_KEY=votre_clé`"
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

if prompt := st.chat_input("Posez votre question ici…"):
    st.session_state.messages.append(new_user_message(prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Réponse en cours…"):
                answer: AIMessage = reply(st.session_state.messages)
            st.markdown(answer.content)
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")
            answer = AIMessage(content="")
        else:
            st.session_state.messages.append(answer)
