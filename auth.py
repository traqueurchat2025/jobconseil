
import streamlit as st
from supabase import create_client, Client
import os

# Charger les identifiants Supabase à partir des secrets Streamlit
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Créer le client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    st.subheader("🔐 Connexion à JobConseil")
    email = st.text_input("📧 Entrez votre e-mail", placeholder="exemple@mail.com")

    if st.button("🔓 Envoyer le lien de connexion"):
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("📩 Lien de connexion envoyé ! Vérifie tes mails.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi du lien : {e}")

    # Vérifie si l'utilisateur est déjà connecté via le lien magique
    user = supabase.auth.get_user()
    if user and user.user:
        st.success(f"✅ Connecté en tant que : {user.user.email}")
        return user.user.email
    else:
        return None
