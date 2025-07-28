import streamlit as st
import openai
from supabase import create_client

# 📦 Supabase config
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧠 Vérifie si l'utilisateur est premium (simplifié)
def is_user_premium(email):
    return email and email.endswith("@pro.fr")

# 🔐 Authentification
def login():
    st.session_state["auth_mode"] = "login"
    email = st.text_input("✉️ Ton e-mail", key="login_email")
    if st.button("📩 Envoyer le lien de connexion"):
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("Lien de connexion envoyé. Vérifie ta boîte mail.")
        except Exception as e:
            st.error(f"Erreur d'envoi : {e}")

def logout():
    if st.button("🚪 Se déconnecter"):
        st.session_state.pop("user_email", None)
        st.success("Déconnecté avec succès.")

# 🔁 Layout
st.set_page_config(page_title="JobConseil – Assistant Droit du Travail", layout="centered")
st.title("📘 JobConseil – Assistant Droit du Travail 🇫🇷")

# 🔑 Authentification utilisateur
user_email = st.session_state.get("user_email", None)

if not user_email:
    st.info("🔐 Connecte-toi pour poser une question.")
    login()
else:
    st.success(f"✅ Connecté en tant que : {user_email}")
    logout()

# 💎 Badge GPT
if user_email:
    if is_user_premium(user_email):
        st.success("💎 Vous utilisez GPT‑4 Turbo (Premium)")
    else:
        st.info("🧠 Vous utilisez GPT‑3.5 (Gratuit)")

# 🎨 CSS design cartes
st.markdown("""
<style>
.card { border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 10px; transition: transform .3s; text-align: center; }
.card:hover { transform: scale(1.03); }
.card-free { background: #f9f9f9; border: 2px solid #ccc; }
.card-prem { background: #fff8e1; border: 2px solid gold; }
.container { display: flex; justify-content: center; flex-wrap: wrap; }
</style>
""", unsafe_allow_html=True)

# 🧠 Cartes GPT
st.markdown("""
<div class="container">
  <div class="card card-free">
    <h3>🧠 GPT‑3.5 Gratuit</h3>
    <ul>
      <li>Réponses rapides</li>
      <li>Compréhension basique</li>
      <li>Droit du travail limité</li>
      <li>100% gratuit</li>
    </ul>
  </div>
  <div class="card card-prem">
    <h3>💎 GPT‑4 Turbo Premium</h3>
    <ul>
      <li>Réponses ultra précises</li>
      <li>Analyse avancée</li>
      <li>Données mises à jour</li>
      <li>9,99 €/mois</li>
    </ul>
  </div>
</div>
""", unsafe_allow_html=True)

# 📤 Requête GPT
def get_gpt_model(email):
    return "gpt-4-turbo" if is_user_premium(email) else "gpt-3.5-turbo"

def ask_gpt(question, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant juridique spécialisé en droit du travail français. Réponds clairement, simplement et concrètement."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur : {e}"

# 📥 Question juridique en temps réel
question = st.text_input("❓ Pose ta question sur le droit du travail (arrêt maladie, licenciement...)")

if user_email and question:
    model = get_gpt_model(user_email)
    reponse = ask_gpt(question, model)
    st.success("✅ Réponse de l’assistant :")
    st.markdown(reponse)
elif question and not user_email:
    st.warning("🛑 Connecte-toi pour obtenir une réponse.")

# 🔽 Bouton vers offres d'emploi
st.markdown("""
<div style="text-align:center; margin-top:40px;">
  <a href="#emploi" style="text-decoration:none;">
    <button style="padding:14px 24px; background:#0078d4; color:white; border:none; border-radius:8px; font-size:17px;">
      🔎 Consulter les offres d'emploi
    </button>
  </a>
</div>
""", unsafe_allow_html=True)

# 📂 Section emploi
st.markdown('<h2 id="emploi">🔍 Offres d\'emploi (optionnel)</h2>', unsafe_allow_html=True)
with st.expander("Rechercher un emploi via France Travail"):
    metier = st.text_input("Métier recherché", "aide-soignant")
    lieu = st.text_input("Code postal ou commune", "28000")
    rayon = st.slider("Rayon (km)", min_value=0, max_value=100, value=20)
    if st.button("🔍 Rechercher les offres"):
        st.info("🚧 Fonctionnalité en cours de développement.")
