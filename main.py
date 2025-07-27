import streamlit as st
from supabase import create_client, Client
import urllib.parse
from auth import login
import openai

# 🎯 Clés secrètes depuis secrets.toml
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# 🔧 Initialiser Supabase et OpenAI
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

# ✅ Authentification avec lien magique
query_params = st.query_params
access_token = query_params.get("access_token", None)

if access_token:
    try:
        user = supabase.auth.get_user(access_token).user
        st.session_state["user"] = user
        st.success(f"👋 Bienvenue, {user['email']} !")
    except Exception as e:
        st.warning("⚠️ Erreur lors de la connexion avec le token.")

# ⏱️ Afficher la barre latérale
st.sidebar.title("👤 Mon compte")
if "user" in st.session_state:
    st.sidebar.success(f"Connecté : {st.session_state['user']['email']}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state.clear()
        st.experimental_rerun()
else:
    login()

# 🏠 Accueil principal
st.title("Bienvenue sur JobConseil 👋")
st.markdown("""
Votre assistant intelligent pour :
- 🤖 Trouver des réponses sur le droit du travail  
- 📄 Créer un CV professionnel  
- ✉️ Rédiger une lettre de motivation  
- 🔍 Rechercher des offres d'emploi en direct
""")

# 💬 Assistant IA si connecté
if "user" in st.session_state:
    st.header("Assistant IA")
    question = st.text_input("Posez votre question (droit du travail, CV, etc.)")
    if st.button("Envoyer") or st.session_state.get("send_with_enter"):
        if question:
            with st.spinner("⏳ L'assistant réfléchit..."):
                try:
                    model = "gpt-4" if st.session_state['user']['email'].endswith("@premium.com") else "gpt-3.5-turbo"
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "Tu es un expert du droit du travail français, création de CV, lettres et offres d'emploi."},
                            {"role": "user", "content": question}
                        ]
                    )
                    st.success("Réponse IA :")
                    st.write(response["choices"][0]["message"]["content"])
                except Exception as e:
                    st.error(f"Erreur IA : {e}")
else:
    st.info("🔐 Connectez-vous pour accéder à l'assistant IA")

# 📊 Comparatif des offres
st.markdown("""
## Nos Offres
| Fonctionnalité                        | Gratuit | Premium |
|--------------------------------------|:-------:|:-------:|
| Assistant IA (droit, CV, lettres…)    |   ✅    |   ✅    |
| Générateur de CV / lettres            |   ✅    |   ✅    |
| Historique des conversations          |   ❌    |   ✅    |
| GPT-4 Turbo                           |   ❌    |   ✅    |
| Support prioritaire                   |   ❌    |   ✅    |
| **Prix**                              |  0 €    | 9,99 €/mois |
""")
