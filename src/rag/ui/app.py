import streamlit as st
import requests

API_BASE = "http://localhost:8000/rag"

st.set_page_config(page_title="RAG Explorer", layout="wide")

st.title("🚀 RAG Prototype — Elasticsearch + FastAPI + Streamlit")

query = st.text_input("Pose ta question :", placeholder="Ex: site down Kedougou")
k = st.slider("Nombre de résultats à récupérer", 1, 10, 5)

if st.button("Rechercher"):
    if not query:
        st.warning("Entre une question.")
    else:
        with st.spinner("Recherche en cours..."):
            try:
                res = requests.get(f"{API_BASE}/ask", params={"q": query, "k": k})
                data = res.json()

                st.subheader("🧠 Réponse générée")
                st.write(data["answer"])

                st.subheader("📄 Résultats bruts")
                st.json(data["raw"])

            except Exception as e:
                st.error(f"Erreur: {e}")
