import streamlit as st
from supabase import create_client
from urllib.parse import parse_qs

# 🔐 Clés Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    access_token = st.query_params.get("access_token", None)

    # Si un lien magique contient un token et qu'on n'est pas encore connecté
    if access_token and "user" not in st.session_state:
        try:
            user = supabase.auth.get_user(access_token)
            if user:
                st.session_state["user"] = user
                st.experimental_rerun()  # Recharge la page avec session active
        except Exception as e:
            st.error(f"❌ Erreur récupération utilisateur : {e}")

    # Si l'utilisateur est déjà connecté
    if "user" in st.session_state:
        return st.session_state["user"]

    # Sinon, on affiche le formulaire
    st.subheader("🔐 Connexion à JobConseil")
    email = st.text_input("📧 Entrez votre e-mail", placeholder="votre@email.com")
    if st.button("Envoyer le lien de connexion") and email:
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("📨 Lien magique envoyé. Vérifie ta boîte mail.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi : {e}")
    return None
