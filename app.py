import streamlit as st
from supabase import create_client, Client
import extra_streamlit_components as stx
from datetime import datetime
import json

# Configuration de Supabase
SUPABASE_URL = "https://rgnspobdngpqjbmjuxqf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnbnNwb2JkbmdwcWpibWp1eHFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgwNzI1NDMsImV4cCI6MjA1MzY0ODU0M30.wOyC3kI-d1Z0lTN1W8PJu6jPJ4voVUgiTTZkotEnWj4"


class SupabaseManager:
    def __init__(self):
        self.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
    def sign_up(self, email: str, password: str):
        try:
            response = self.supabase_client.auth.sign_up({
                "email": email,
                "password": password
            })
            return True, response
        except Exception as e:
            return False, str(e)
    
    def sign_in(self, email: str, password: str):
        try:
            response = self.supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return True, response
        except Exception as e:
            return False, str(e)
    
    def sign_out(self):
        try:
            self.supabase_client.auth.sign_out()
            return True, "Déconnexion réussie"
        except Exception as e:
            return False, str(e)
            
    def get_user(self):
        try:
            return self.supabase_client.auth.get_user()
        except:
            return None
            
    def save_submission(self, nom: str, prenom: str, email: str, lien: str):
        try:
            data = {
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'lien_article': lien,
                'date_soumission': datetime.now().isoformat()
            }
            response = self.supabase_client.table('soumissions').insert(data).execute()
            return True, "Soumission enregistrée avec succès!"
        except Exception as e:
            return False, f"Erreur lors de l'enregistrement: {str(e)}"

def initialize_session_state():
    """Initialise les variables de session"""
    if 'supabase' not in st.session_state:
        st.session_state.supabase = SupabaseManager()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def login_page():
    """Page de connexion"""
    st.title("🔐 BMU - Envio de artigos")
    
    
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")
            submit_login = st.form_submit_button("Se connecter")
            
            if submit_login:
                if email and password:
                    success, response = st.session_state.supabase.sign_in(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.success("Connexion réussie!")
                        st.rerun()
                    else:
                        st.error(f"Erreur de connexion: {response}")
                else:
                    st.error("Veuillez remplir tous les champs")
    
    with tab2:
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Senha", type="password", key="signup_password")
            password_confirm = st.text_input("Repetir a senha", type="password")
            submit_signup = st.form_submit_button("Se inscrever")
            
            if submit_signup:
                if email and password and password_confirm:
                    if password == password_confirm:
                        success, response = st.session_state.supabase.sign_up(email, password)
                        if success:
                            st.success("Inscription réussie! Veuillez vérifier votre email")
                        else:
                            st.error(f"Erreur d'inscription: {response}")
                    else:
                        st.error("Les mots de passe ne correspondent pas")
                else:
                    st.error("Veuillez remplir tous les champs")

def submission_page():
    """Page de soumission d'articles"""
    st.title("📝 Soumission d'Articles")
    
    # Bouton de déconnexion
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Déconnexion"):
            success, message = st.session_state.supabase.sign_out()
            if success:
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.rerun()
            else:
                st.error(message)
    
    with col1:
        st.write(f"Connecté en tant que: {st.session_state.user_email}")
    
    st.markdown("---")
    
    # Formulaire de soumission
    with st.form("submission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *", key="nom")
            email = st.text_input("Email *", key="email", 
                                value=st.session_state.user_email, disabled=True)
        
        with col2:
            prenom = st.text_input("Prénom *", key="prenom")
            lien = st.text_input("Lien vers l'article *", key="lien")

        submitted = st.form_submit_button("Soumettre")
        
        if submitted:
            if not all([nom, prenom, lien]):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                success, message = st.session_state.supabase.save_submission(
                    nom, prenom, st.session_state.user_email, lien
                )
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="Soumissions d'Articles",
        page_icon="📝",
        layout="centered"
    )

    # Initialisation des variables de session
    initialize_session_state()
    
    # Affichage de la page appropriée selon l'état d'authentification
    if not st.session_state.authenticated:
        login_page()
    else:
        submission_page()

if __name__ == "__main__":
    main()
