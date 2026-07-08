import streamlit as st
import dns.resolver
_new_resolver = dns.resolver.Resolver()
_new_resolver.nameservers = ['8.8.8.8', '1.1.1.1']
dns.resolver.default_resolver = _new_resolver
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
import os

try:
    MONGO_URI = st.secrets["MONGO_URI"]
    DB_NAME = st.secrets["DB_NAME"]
except (KeyError, FileNotFoundError):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "gestion_etudiants")
COLLECTION_NAME = "etudiants"


@st.cache_resource
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]


collection = get_db()


def inserer_etudiant(numero, nom_prenom, age, classe, moyenne):
    return collection.insert_one({
        "numero": numero,
        "nom_prenom": nom_prenom,
        "age": age,
        "classe": classe,
        "moyenne": moyenne
    })


def rechercher_etudiants(terme=""):
    query = {}
    if terme:
        query["$or"] = [
            {"numero": {"$regex": terme, "$options": "i"}},
            {"nom_prenom": {"$regex": terme, "$options": "i"}},
            {"classe": {"$regex": terme, "$options": "i"}},
        ]
    return list(collection.find(query))


def modifier_etudiant(etudiant_id, numero, nom_prenom, age, classe, moyenne):
    collection.update_one(
        {"_id": ObjectId(etudiant_id)},
        {"$set": {
            "numero": numero,
            "nom_prenom": nom_prenom,
            "age": age,
            "classe": classe,
            "moyenne": moyenne
        }}
    )


def supprimer_etudiant(etudiant_id):
    collection.delete_one({"_id": ObjectId(etudiant_id)})


st.set_page_config(page_title="Gestion des Etudiants", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #f5f5f7;
        --bg-secondary: #ffffff;
        --bg-sidebar: #1d1d1f;
        --text-primary: #1d1d1f;
        --text-secondary: #86868b;
        --accent-blue: #007aff;
        --accent-green: #34c759;
        --accent-red: #ff3b30;
        --border-color: #d2d2d7;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
        --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }

    .stApp {
        background-color: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    }

    .stApp > header {
        background: transparent !important;
    }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    .stHeader {
        background: transparent !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    h1 { font-size: 2.2rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.15) !important;
    }

    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        background: var(--bg-primary) !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #0066d6 !important;
    }

    div[data-testid="stForm"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
        box-shadow: var(--shadow-md) !important;
        max-width: 700px !important;
        margin: 0 auto !important;
    }

    .stRadio > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 6px !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stRadio > div > div {
        gap: 4px !important;
    }

    .stRadio > div > div > label {
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stRadio > div > div > label:hover {
        background: var(--bg-primary) !important;
    }

    .stRadio > div > div > div[data-checked="true"] > label {
        background: var(--accent-blue) !important;
        color: white !important;
        border-radius: var(--radius-sm) !important;
    }

    .stDataFrame {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-md) !important;
        border: 1px solid var(--border-color) !important;
    }

    .stDataFrame > div {
        border-radius: var(--radius-md) !important;
    }

    .stSuccess {
        background: rgba(52, 199, 89, 0.1) !important;
        border: 1px solid rgba(52, 199, 89, 0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: #1a7f37 !important;
    }

    .stError {
        background: rgba(255, 59, 48, 0.1) !important;
        border: 1px solid rgba(255, 59, 48, 0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: #cf222e !important;
    }

    .stInfo {
        background: rgba(0, 122, 255, 0.1) !important;
        border: 1px solid rgba(0, 122, 255, 0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: #0066d6 !important;
    }

    [data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: none !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > label {
        color: rgba(255,255,255,0.8) !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 16px !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > label:hover {
        background: rgba(255,255,255,0.1) !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > div[data-checked="true"] > label {
        background: var(--accent-blue) !important;
        color: white !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    div[data-testid="stExpander"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        background: var(--bg-secondary) !important;
        border-radius: var(--radius-md) !important;
        padding: 4px !important;
        border: 1px solid var(--border-color) !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        padding: 10px 20px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }

    .stMetric {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 20px !important;
        box-shadow: var(--shadow-sm) !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        margin-bottom: 6px !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stDataFrame"] table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
    }

    [data-testid="stDataFrame"] th {
        background: var(--bg-primary) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em !important;
        color: var(--text-secondary) !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    [data-testid="stDataFrame"] td {
        padding: 12px 16px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    [data-testid="stDataFrame"] tr:hover td {
        background: var(--bg-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🎓 Gestion Étudiants")
    st.markdown('<p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Application de gestion</p>', unsafe_allow_html=True)
    st.markdown("---")

page = st.radio("Navigation", ["Liste", "Ajouter", "Modifier"], horizontal=True, label_visibility="collapsed")

if page == "Liste":
    st.markdown("# 📋 Liste des Etudiants")
    st.markdown('<p style="color: #86868b; margin-top: -10px; font-size: 0.95rem;">Gérez votre base de données d\'étudiants</p>', unsafe_allow_html=True)

    terme = st.text_input("Rechercher", placeholder="Numéro, nom ou classe...", label_visibility="collapsed")
    etudiants = rechercher_etudiants(terme)

    if etudiants:
        import pandas as pd
        df = pd.DataFrame(etudiants)
        df = df[["numero", "nom_prenom", "age", "classe", "moyenne"]].rename(columns={
            "numero": "N°", "nom_prenom": "Nom & Prénom", "age": "Âge", "classe": "Classe", "moyenne": "Moyenne"
        })
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True, hide_index=False)

        st.markdown("---")
        st.markdown("### ⚡ Actions rapides")

        col1, col2 = st.columns([3, 1])
        with col1:
            selected_numero = st.selectbox("Sélectionner un étudiant", [e.get("numero", "") for e in etudiants])
        with col2:
            action = st.radio("Action", ["Modifier", "Supprimer"], horizontal=True, label_visibility="collapsed")

        etudiant_choisi = next((e for e in etudiants if e.get("numero") == selected_numero), None)

        if etudiant_choisi:
            col_a, col_b = st.columns(2)
            with col_a:
                if action == "Modifier":
                    if st.button("✏️ Ouvrir la modification", use_container_width=True):
                        st.session_state.editing_id = str(etudiant_choisi["_id"])
                        st.session_state.page = "Modifier"
                        st.rerun()
            with col_b:
                if action == "Supprimer":
                    if st.button("🗑️ Supprimer", type="primary", use_container_width=True):
                        supprimer_etudiant(etudiant_choisi["_id"])
                        st.success(f"{etudiant_choisi.get('nom_prenom', '')} supprimé.")
                        st.rerun()
    else:
        st.info("Aucun étudiant trouvé.")

elif page == "Ajouter":
    st.markdown("# ➕ Ajouter un Etudiant")
    st.markdown('<p style="color: #86868b; margin-top: -10px; font-size: 0.95rem;">Remplissez les informations pour créer un nouveau profil</p>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            numero = st.text_input("Numéro d'inscription *", placeholder="Ex: 2024-001")
            nom_prenom = st.text_input("Nom & Prénom *", placeholder="Ex: Dupont Jean")
        with col2:
            age = st.number_input("Âge *", min_value=10, max_value=100, value=18)
            classe = st.selectbox("Classe *", ["", "1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"])

        moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=10.0, step=0.01, format="%.2f")

        submitted = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)

        if submitted:
            if not numero or not nom_prenom or not classe:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                existing = collection.find_one({"numero": numero})
                if existing:
                    st.error(f"Le numéro {numero} existe déjà.")
                else:
                    inserer_etudiant(numero, nom_prenom, age, classe, moyenne)
                    st.success(f"{nom_prenom} ajouté avec succès !")
                    st.balloons()

elif page == "Modifier":
    etudiant_id = st.session_state.get("editing_id")
    etudiant = collection.find_one({"_id": ObjectId(etudiant_id)}) if etudiant_id else None

    if not etudiant:
        st.markdown("# ⚠️ Aucun étudiant sélectionné")
        st.markdown('<p style="color: #86868b; margin-top: -10px; font-size: 0.95rem;">Retournez à la liste et sélectionnez un étudiant à modifier</p>', unsafe_allow_html=True)
    else:
        st.markdown(f"# ✏️ Modifier : {etudiant.get('nom_prenom', '')}")
        st.markdown('<p style="color: #86868b; margin-top: -10px; font-size: 0.95rem;">Mettez à jour les informations de l\'étudiant</p>', unsafe_allow_html=True)

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                numero = st.text_input("Numéro d'inscription *", value=etudiant.get("numero", ""))
                nom_prenom = st.text_input("Nom & Prénom *", value=etudiant.get("nom_prenom", ""))
            with col2:
                age = st.number_input("Âge *", min_value=10, max_value=100, value=etudiant.get("age", 18))
                classes_list = ["1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"]
                current_class = etudiant.get("classe", "")
                classe = st.selectbox("Classe *", classes_list, index=classes_list.index(current_class) if current_class in classes_list else 0)

            moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=float(etudiant.get("moyenne", 10.0)), step=0.01, format="%.2f")

            submitted = st.form_submit_button("💾 Enregistrer les modifications", type="primary", use_container_width=True)

            if submitted:
                if not numero or not nom_prenom or not classe:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    if numero != etudiant.get("numero"):
                        existing = collection.find_one({"numero": numero})
                        if existing:
                            st.error(f"Le numéro {numero} existe déjà.")
                        else:
                            modifier_etudiant(etudiant_id, numero, nom_prenom, age, classe, moyenne)
                            st.success(f"{nom_prenom} modifié !")
                            st.session_state.pop("editing_id", None)
                            st.rerun()
                    else:
                        modifier_etudiant(etudiant_id, numero, nom_prenom, age, classe, moyenne)
                        st.success(f"{nom_prenom} modifié !")
                        st.session_state.pop("editing_id", None)
                        st.rerun()
