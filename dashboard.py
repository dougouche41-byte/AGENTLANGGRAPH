import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Assistant TrustHariz", page_icon="🤖", layout="centered")

st.title("Assistant TrustHariz")
st.caption("Mode multi-agents : Chef + Finance + Mémoire")

user_input = st.text_area("Posez votre demande ici :", height=120)

if st.button("Lancer l'analyse"):
    if not user_input.strip():
        st.warning("Veuillez écrire une demande.")
    else:
        with st.spinner("Les agents travaillent..."):
            result = run_agent(user_input)

        st.subheader("Mission")
        st.success(result["mission"])

        st.subheader("Finance")
        st.info("Analyse financière")
        st.json(result["finance"])

        st.subheader("Mémoire")
        st.info("Préparation mémoire")
        st.json(result["memory"])