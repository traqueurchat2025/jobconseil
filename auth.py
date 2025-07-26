import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    st.subheader("🔐 Connexion à JobConseil")
    email = st.text_input("📧 Entrez votre e-mail", placeholder="votre@email.com")

    if st.button("Envoyer le lien magique"):
        try:
            supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    # Forcer l'URL de redirection vers ton app
                    "emailRedirectTo": "https://jobconseil-pboggnsbx8iwxjanoefcyy.streamlit.app"
                }
            })
            st.success("📨 Lien magique envoyé ! Vérifiez votre boîte mail.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi du lien : {e}")
