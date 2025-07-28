import streamlit as st
import openai

# 🔐 Simulation simple : premium si email finit par "@pro.fr"
def is_user_premium(email):
    return email and email.endswith("@pro.fr")

st.set_page_config(page_title="JobConseil – Assistant Droit du Travail", layout="wide")
st.title("📘 JobConseil – Assistant Droit du Travail 🇫🇷")

# Authentification
user_email = st.session_state.get("user_email", None)
if user_email:
    if is_user_premium(user_email):
        st.success("💎 Vous utilisez GPT‑4 Turbo (Premium)")
    else:
        st.info("🧠 Vous utilisez GPT‑3.5 (Gratuit)")
else:
    st.warning("🔐 Veuillez vous connecter pour accéder à l'assistant juridique.")

# 🎨 CSS pour les cartes visuelles
st.markdown("""
<style>
.card { border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 10px; transition: transform .3s; }
.card:hover { transform: scale(1.03); }
.card-free { background: #f9f9f9; border: 2px solid #ccc; }
.card-prem { background: #fff8e1; border: 2px solid gold; }
.container { display: flex; justify-content: center; flex-wrap: wrap; }
.button-prem { padding: 12px 20px; background: gold; color: #222; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# 🧠 Cartes GPT-3.5 / GPT-4
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
    <button class="button-prem">Passer à GPT‑4 Premium</button>
  </div>
</div>
""", unsafe_allow_html=True)

# 🔍 Choix du modèle
def get_gpt_model(email):
    return "gpt-4-turbo" if is_user_premium(email) else "gpt-3.5-turbo"

# ⚙️ Requête à OpenAI
def ask_gpt(question, model):
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant juridique spécialisé en droit du travail français. Réponds toujours clairement et simplement."},
                {"role": "user", "content": question}
            ]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur : {e}"

# 📝 Zone de question juridique
st.markdown("---")
question = st.text_input("❓ Posez votre question sur vos droits (ex : licenciement, arrêt maladie...)")
if st.button("💼 Obtenir une réponse juridique"):
    if user_email and question:
        model = get_gpt_model(user_email)
        answer = ask_gpt(question, model)
        st.success("✅ Réponse :")
        st.markdown(answer)
    else:
        st.warning("Vous devez être connecté et saisir une question.")

# 🔁 Bouton vers offres d’emploi
st.markdown("""
<div style="text-align:center; margin-top:40px;">
  <a href="#emploi" style="text-decoration:none;">
    <button style="padding:14px 24px; background:#0078d4; color:white; border:none; border-radius:8px; font-size:17px;">
      🔎 Consulter les offres d'emploi
    </button>
  </a>
</div>
""", unsafe_allow_html=True)

# 📂 Section emploi en bas
st.markdown('<h2 id="emploi">🔍 Offres d\'emploi (optionnel)</h2>', unsafe_allow_html=True)
with st.expander("Rechercher un emploi via France Travail"):
    metier = st.text_input("Métier recherché", "aide‑soignant")
    lieu = st.text_input("Code postal ou commune", "28000")
    rayon = st.slider("Rayon (km)", min_value=0, max_value=100, value=20)
    if st.button("🔍 Rechercher les offres"):
        st.info("🚧 Fonctionnalité de recherche d’emploi bientôt disponible.")
