import streamlit as st
import requests
import base64

st.set_page_config(page_title="JobConseil – Offres d'emploi", page_icon="💼")

st.title("💼 JobConseil – Recherche d'offres d'emploi")
st.markdown("Trouvez rapidement les dernières offres disponibles via France Travail")

# --------------------------
# Fonction pour récupérer le token France Travail
# --------------------------
def get_token_france_travail():
    client_id = st.secrets["PE_CLIENT_ID"]
    client_secret = st.secrets["PE_CLIENT_SECRET"]
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("❌ Erreur lors de la récupération du token")
        st.code(response.text)
        return None

# --------------------------
# Interface utilisateur
# --------------------------
metier = st.text_input("🔤 Métier recherché", "aide-soignant")
code_postal = st.text_input("📍 Code postal ou commune", "28000")
rayon = st.slider("📏 Rayon de recherche (en km)", 0, 100, 20)

if st.button("🔎 Rechercher les offres"):
    token = get_token_france_travail()

    if token:
        st.success("✅ Connexion établie avec France Travail")

        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "motsCles": metier,
            "commune": code_postal,
            "distance": rayon
        }

        url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            offres = response.json().get("resultats", [])

            if offres:
                st.subheader("📋 Offres trouvées :")
                for offre in offres:
                    st.markdown(f"### {offre.get('intitule', 'Intitulé inconnu')}")
                    st.write("📍", offre.get("lieuTravail", {}).get("libelle", "Lieu inconnu"))
                    st.write("📝", offre.get("description", "")[:300] + "...")
                    st.markdown("---")
            else:
                st.info("Aucune offre trouvée pour ces critères.")
        else:
            st.error("❌ Erreur lors de la récupération des offres")
            st.code(response.text)
