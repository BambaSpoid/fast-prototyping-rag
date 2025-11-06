import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000/rag"

st.set_page_config(page_title="Assistant Réseau IA", layout="wide")

st.title("🧠 Assistant NOC – Elasticsearch + Ollama")

st.markdown(
    "Pose une question sur les incidents réseau (ex. **site down kedougou**, "
    "**link failure**, **alarme major Dakar**...)"
)

# --- Entrée utilisateur
query = st.text_input("👉 Question :", placeholder="site down kedougou")
k = st.slider("Nombre de documents à utiliser :", 1, 10, 5)

if st.button("Analyser") and query:
    with st.spinner("Analyse en cours..."):
        try:
            res = requests.get(
                f"{API_BASE}/ask", params={"q": query, "k": k}, timeout=120
            )
            data = res.json()

            # --- Réponse IA
            st.subheader("💬 Réponse générée par Ollama")
            st.markdown(f"```\n{data['answer']}\n```")

            # --- Contexte (incidents trouvés)
            st.subheader("📚 Contexte (incidents utilisés)")
            context = data.get("context", [])
            if context:
                df = pd.DataFrame(context)
                st.dataframe(df[["when", "severity", "site", "score", "text"]])
            else:
                st.info("Aucun document trouvé dans Elasticsearch.")

        except Exception as e:
            st.error(f"Erreur : {e}")
