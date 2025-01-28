import streamlit as st
import supabase
from datetime import datetime

# Configuration de Supabase
SUPABASE_URL = "https://rgnspobdngpqjbmjuxqf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnbnNwb2JkbmdwcWpibWp1eHFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgwNzI1NDMsImV4cCI6MjA1MzY0ODU0M30.wOyC3kI-d1Z0lTN1W8PJu6jPJ4voVUgiTTZkotEnWj4"

# Initialisation de la connexion Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_session_state():
    """Initialise les variables de session"""
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

def save_submission(nom, prenom, email, lien):
    """Sauvegarde la soumission dans Supabase"""
    try:
        data = {
            'nom': nom,
            'prenom': prenom,
            'email': email,
            'lien_article': lien,
            'date_soumission': datetime.now().isoformat()
        }
        
        response = supabase_client.table('soumissions').insert(data).execute()
        return True, "Soumission enregistrée avec succès!"
    except Exception as e:
        return False, f"Erreur lors de l'enregistrement: {str(e)}"

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="Soumissions d'Articles",
        page_icon="📝",
        layout="centered"
    )

    # Initialisation des variables de session
    initialize_session_state()

    # Titre principal
    st.title("📝 Soumission d'Articles")
    st.markdown("---")

    # Formulaire de soumission
    with st.form("submission_form"):
        # Champs du formulaire
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *", key="nom")
            email = st.text_input("Email *", key="email")
        
        with col2:
            prenom = st.text_input("Prénom *", key="prenom")
            lien = st.text_input("Lien vers l'article *", key="lien")

        # Bouton de soumission
        submitted = st.form_submit_button("Soumettre")

        if submitted:
            # Vérification des champs obligatoires
            if not all([nom, prenom, email, lien]):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                # Validation basique de l'email
                if '@' not in email:
                    st.error("Veuillez entrer une adresse email valide.")
                else:
                    # Sauvegarde dans Supabase
                    success, message = save_submission(nom, prenom, email, lien)
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        # Réinitialisation du formulaire
                        st.session_state.submitted = True
                    else:
                        st.error(message)

    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ Information")
    st.markdown("""
    * Tous les champs marqués d'un astérisque (*) sont obligatoires
    * Assurez-vous que le lien vers l'article est valide et accessible
    * Vous recevrez une confirmation par email après la validation de votre soumission
    """)

if __name__ == "__main__":
    main()
