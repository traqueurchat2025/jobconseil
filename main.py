
import streamlit as st
import openai

st.set_page_config(page_title="JobConseil", layout="wide")

st.sidebar.title("📋 JobConseil")
page = st.sidebar.radio("Navigation", [
    "Accueil", "Assistant IA", "Créer un CV", "Lettre de motivation", "Offres d'emploi", "Mon compte"
])

# Simuler un abonnement premium
abonne_premium = st.sidebar.checkbox("✅ Je suis abonné Premium (simulateur)")

# Définir les prompts selon le niveau d'abonnement
def get_system_prompt(premium: bool):
    if premium:
        return (
            "Tu es un conseiller expert en droit du travail français. Réponds de manière claire, structurée et complète. "
            "Donne des explications légales, les droits du salarié, les étapes à suivre, et si besoin un exemple de lettre ou de procédure."
        )
    else:
        return (
            "Tu es un assistant généraliste. Réponds simplement et rapidement, sans entrer dans les détails juridiques complexes."
        )

# Obtenir une réponse de l'IA selon le modèle
def ai_response(prompt, premium=False):
    try:
        model = "gpt-4" if premium else "gpt-3.5-turbo"
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": get_system_prompt(premium)},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        if not premium:
            content += "\n\n🛑 Tu veux une réponse plus détaillée ? Active l’abonnement premium (GPT-4) sur JobConseil pour tout débloquer."
        return content
    except Exception as e:
        return f"Erreur IA : {e}"

if page == "Accueil":
    st.title("Bienvenue sur JobConseil 👋")
    st.markdown("""Votre assistant intelligent pour :
- 🤖 Trouver des réponses sur le droit du travail  
- 📄 Créer un CV professionnel  
- ✉️ Rédiger une lettre de motivation  
- 🔍 Rechercher des offres d'emploi en direct""")
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
    st.title("Assistant IA")
    st.markdown("Posez votre question (droit du travail, CV, etc.)")

    question = st.text_input("💬 Votre question :", placeholder="Ex : Que faire en cas de licenciement abusif ?", label_visibility="collapsed")

    if question:
        with st.spinner("🤖 L'assistant réfléchit..."):
            reponse = ai_response(question, premium=abonne_premium)
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
