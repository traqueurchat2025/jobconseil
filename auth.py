import streamlit as st
from supabase import create_client
from urllib.parse import parse_qs

# 🔐 Configuration Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    query_params = st.query_params  # ✅ Nouvelle version
    access_token = query_params.get("access_token", None)

    if access_token:
        try:
            user = supabase.auth.get_user(access_token)
            if user:
                st.session_state["user"] = user
                return user
        except Exception as e:
            st.error(f"❌ Erreur récupération utilisateur : {e}")

    elif "user" in st.session_state:
        return st.session_state["user"]

    # Formulaire de connexion
    st.subheader("🔐 Connexion à JobConseil")
    email = st.text_input("📧 Entrez votre e-mail", placeholder="votre@email.com")
    if st.button("Envoyer le lien de connexion") and email:
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("📨 Lien magique envoyé. Vérifie ta boîte mail.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi : {e}")
    return None
