
import streamlit as st
import os

st.set_page_config(page_title="JobConseil", layout="wide")
st.sidebar.title("📋 JobConseil")
page = st.sidebar.radio("Navigation", [
    "Accueil", "Assistant IA", "Créer un CV", "Lettre de motivation", "Offres d'emploi", "Mon compte"
])

# Vérification simple gratuite/premium (simulée ici)
abonne_premium = st.sidebar.checkbox("✅ Je suis abonné Premium (simulateur)")

def ai_response(prompt, model="gpt-3.5-turbo"):
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un conseiller emploi et droit du travail"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erreur IA : {e}"

if page == "Accueil":
    st.title("Bienvenue sur JobConseil 👋")
    st.markdown("""
    #### Votre assistant intelligent pour :
    - 🤖 Trouver des réponses sur le droit du travail
    - 📄 Créer un CV professionnel
    - ✉️ Rédiger une lettre de motivation
    - 🔍 Rechercher des offres d’emploi en direct
    """)
    st.markdown("---")
    st.subheader("Nos Offres")

    st.markdown("""
    | Fonctionnalité                                | Gratuit | Premium |
    |----------------------------------------------|:-------:|:-------:|
    | Assistant IA (droit, CV, lettres…)            | ✅      | ✅      |
    | Générateur de CV / lettres                    | ✅      | ✅      |
    | Historique des conversations                  | ❌      | ✅      |
    | GPT-4 Turbo                                   | ❌      | ✅      |
    | Support prioritaire                           | ❌      | ✅      |
    | Prix                                          | 0 €     | 9,99 €/mois |
    """)

elif page == "Assistant IA":
    st.title("💬 Assistant IA")
    question = st.text_area("Posez votre question (droit du travail, CV, etc.)")
    if st.button("Envoyer"):
        if abonne_premium:
            reponse = ai_response(question, model="gpt-4")
        else:
            reponse = ai_response(question)
        st.markdown("### 🤖 Réponse de l'assistant :")
        st.write(reponse)

elif page == "Créer un CV":
    st.title("🧾 Générateur de CV")
    st.info("Fonctionnalité à venir dans la prochaine version.")

elif page == "Lettre de motivation":
    st.title("📨 Générateur de lettre de motivation")
    st.info("Fonctionnalité à venir dans la prochaine version.")

elif page == "Offres d'emploi":
    st.title("🔍 Offres d'emploi")
    st.info("Connexion à Pôle Emploi en cours.")

elif page == "Mon compte":
    st.title("👤 Espace personnel")
    st.info("Connexion / abonnement en cours d'intégration.")
