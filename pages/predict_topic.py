import streamlit as st
import requests
import pandas as pd

# Configuration de la mise en page
st.set_page_config(
    page_title="NLP Topic Modeling",
    page_icon="🧠",
    layout="wide"
)

# En-tête principal avec un titre stylisé
st.title("🧠 Prédiction Topic Modeling")

# Introduction
st.markdown("""
Bienvenue sur l'interface de déploiement du projet **NLP Topic Modeling**.
Utilisez cette application pour tester la connexion à l'API et prédire les thèmes d'un texte à l'aide de modèles de traitement du langage naturel (NLP).
""")

# Section pour tester la connexion avec l'API
st.header("🔌 Tester la connexion à l'API")

# Utilisation de colonnes pour une présentation plus fluide
col1, col2 = st.columns([2, 5])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Lightbulb_icon.svg/2048px-Lightbulb_icon.svg.png", width=100)

with col2:
    # Bouton pour tester la connexion à l'API
    if st.button("🔍 Tester la connexion API"):
        try:
            # URL de l'API pour vérifier son statut
            status_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/status"
            response = requests.get(status_url)

            # Afficher la réponse
            if response.status_code == 200:
                st.success("L'API est en ligne! 🚀")
            else:
                st.error(f"Erreur de connexion à l'API: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de la tentative de connexion: {e}")

# Séparation visuelle
st.markdown("---")

# Section pour faire une prédiction
st.header("📝 Faire une prédiction sur un texte")

# Explication supplémentaire
st.markdown("Entrez un texte dans la zone ci-dessous et obtenez une prédiction sur les topics probables.")

# Utilisation d'une zone de texte pour entrer le texte utilisateur
user_input = st.text_area("💬 Entrez le texte pour lequel vous souhaitez prédire les topics:", height=150)

# Liste statique des thèmes
themes = [
    "Dynamique des Fluides et Énergétique",
    "Physique Quantique et Magnétisme",
    "Apprentissage Automatique et Intelligence Artificielle",
    "Réseaux Neuronaux et Apprentissage Profond",
    "Algorithmes et Théorie de la Complexité",
    "Astrophysique et Formation des Galaxies",
    "Cosmologie et Observation Radio",
    "Modélisation Mathématique et Méthodes Approximatives",
    "Théorie de l'Information et Communication",
    "Analyse des Réseaux Sociaux et des Données"
]

# Fonction pour faire la prédiction
def make_prediction():
    predict_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/predict"
    data = {"text": user_input}
    response = requests.post(predict_url, json=data)

    if response.status_code == 200:
        prediction = response.json()
        topics = prediction.get("topic_distribution", [])

        # Afficher les données pour débogage

        if topics:
            # Convertir les données en DataFrame
            df = pd.DataFrame(topics)
            df["probability"] = df["probability"].apply(lambda x: f"{x:.2f}")
            st.session_state.topics = topics
            st.session_state.prediction_df = df

            # Trouver le thème avec la probabilité la plus élevée
            max_prob_topic = max(topics, key=lambda x: float(x["probability"]))
            st.session_state.predicted_theme = max_prob_topic["theme"]
            st.session_state.predicted_value = st.session_state.predicted_theme  # Garder le thème comme chaîne
            st.success("Prédiction effectuée! 🎉")
        else:
            st.warning("Aucune distribution de topics reçue.")
    else:
        st.error(f"Erreur de prédiction: {response.status_code}")

# Afficher le bouton pour faire la prédiction
if st.button("📊 Valider"):
    if user_input.strip():
        make_prediction()
    else:
        st.warning("⚠️ Veuillez entrer un texte avant de valider.")

# Vérifier si une prédiction a été faite et afficher les résultats
if "prediction_df" in st.session_state:
    st.write("### 📋 Distribution des Topics")
    st.table(st.session_state.prediction_df)

    # Section de feedback
    st.markdown("---")
    st.header("🗣️ Envoyer votre feedback")

    # Menu déroulant pour sélectionner le thème réel parmi la liste statique
    real_value = st.selectbox("🔍 Sélectionnez le thème réel:", themes, index=themes.index(st.session_state.predicted_theme))

    if st.button("📤 Envoyer le feedback"):
        try:
            # URL de l'API pour envoyer le feedback
            feedback_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/feedback_topic"

            # Données à envoyer à l'API
            feedback_data = {
                "text_input": user_input,  # Texte utilisé pour la prédiction
                "predicted_value": st.session_state.predicted_value,  # Le thème prédit
                "real_value": real_value
            }


            # Requête POST pour envoyer le feedback
            feedback_response = requests.post(feedback_url, json=feedback_data)

            # Vérifier la réponse de l'API
            if feedback_response.status_code == 200:
                st.success("Merci pour votre feedback! 👍")
            else:
                st.error(f"Erreur lors de l'envoi du feedback: {feedback_response.status_code}")
                st.write("Réponse de l'API:", feedback_response.json())  # Afficher la réponse d'erreur pour débogage
        except Exception as e:
            st.error(f"Erreur lors de l'envoi du feedback: {e}")
