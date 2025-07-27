import streamlit as st
import requests
import os
from supabase import create_client

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Authentification utilisateur
def connexion_utilisateur():
    st.sidebar.title("🔐 Connexion")
    email = st.sidebar.text_input("📧 Email")
    if st.sidebar.button("📨 Envoyer un lien magique"):
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("📩 Lien envoyé ! Vérifie ta boîte mail.")
        except Exception as e:
            st.error(f"Erreur d'envoi : {e}")

connexion_utilisateur()

# Page principale
st.title("💼 JobConseil – Assistant Emploi IA 🇫🇷")
st.markdown("Trouvez un emploi, un métier, ou rédigez une lettre avec l'IA.")

# Authentification à l’API Pôle Emploi
@st.cache_data(ttl=3600)
def get_access_token():
    client_id = os.getenv("PE_CLIENT_ID")
    client_secret = os.getenv("PE_CLIENT_SECRET")

    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error("❌ Erreur lors de la récupération du token Pôle Emploi")
        return None

# Fonction de recherche
def rechercher_offres(token, mot_cle, code_commune="75001", rayon=10):
    url = f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "motsCles": mot_cle,
        "codeCommune": code_commune,
        "rayon": rayon,
        "tempsPlein": "true",
        "range": "0-10"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("resultats", [])
    else:
        st.error("❌ Erreur lors de la recherche d’offres")
        return []

# Interface recherche
st.subheader("🔍 Recherche d'offres d'emploi")

mot_cle = st.text_input("🔤 Métier recherché", "aide-soignant")
ville = st.text_input("📍 Code postal ou commune", "75001")
rayon = st.slider("📏 Rayon (km)", 0, 100, 10)

if st.button("🔎 Lancer la recherche"):
    token = get_access_token()
    if token:
        offres = rechercher_offres(token, mot_cle, code_commune=ville, rayon=rayon)
        if offres:
            st.success(f"{len(offres)} offre(s) trouvée(s) :")
            for offre in offres:
                st.markdown(f"### {offre['intitule']}")
                st.markdown(f"📍 {offre.get('lieuTravail', {}).get('libelle', 'Lieu inconnu')}")
                st.markdown(f"📝 {offre.get('description', '')[:300]}...")
                url = offre.get('origineOffre', {}).get('urlOrigine', '#')
                st.markdown(f"[👉 Voir l'offre sur Pôle Emploi]({url})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("Aucune offre trouvée.")
