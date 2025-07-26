
import streamlit as st
from auth import login

st.set_page_config(page_title="JobConseil", page_icon="💼")

# Barre latérale
st.sidebar.title("JobConseil")
page = st.sidebar.radio("Navigation", ["Accueil", "Assistant IA", "Mon compte"])

# Page d'accueil
if page == "Accueil":
    st.title("Bienvenue sur JobConseil 👋")
    st.markdown("""
    Votre assistant intelligent pour :
    - 🤖 Trouver des réponses sur le droit du travail  
    - 📄 Créer un CV professionnel  
    - ✉️ Rédiger une lettre de motivation  
    - 🔍 Rechercher des offres d’emploi en direct  
    """)

# Page Assistant IA
elif page == "Assistant IA":
    st.title("Assistant IA")
    question = st.text_input("Posez votre question (droit du travail, CV, etc.)", placeholder="Ex : Ai-je droit au chômage après une rupture conventionnelle ?")

    if question:
        st.info("⏳ L'assistant réfléchit...")
        # Simulation de réponse
        st.success("Réponse IA : (ceci est un exemple) Vous avez droit à l'allocation chômage si...")

# Page Mon compte (connexion)
elif page == "Mon compte":
    st.title("👤 Mon compte")
    user_email = login()
    if user_email:
        st.success(f"Bienvenue {user_email}")
    else:
        st.info("Veuillez vous connecter pour accéder à votre compte.")
