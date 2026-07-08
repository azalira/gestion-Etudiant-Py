import streamlit as st
import dns.resolver
_new_resolver = dns.resolver.Resolver()
_new_resolver.nameservers = ['8.8.8.8', '1.1.1.1']
dns.resolver.default_resolver = _new_resolver
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Gestion des Etudiants", page_icon="🎓", layout="wide")

load_dotenv()

try:
    MONGO_URI = st.secrets["MONGO_URI"]
    DB_NAME = st.secrets["DB_NAME"]
except Exception:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "gestion_etudiants")
COLLECTION_NAME = "etudiants"


@st.cache_resource
def get_db():
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=15000,
        connectTimeoutMS=15000,
        socketTimeoutMS=15000,
        tls=True,
        retryWrites=True
    )
    return client[DB_NAME][COLLECTION_NAME]


collection = get_db()


def generer_numero():
    count = collection.count_documents({})
    return f"ETU-{str(count + 1).zfill(4)}"


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


def modifier_etudiant(etudiant_id, nom_prenom, age, classe, moyenne):
    collection.update_one(
        {"_id": ObjectId(etudiant_id)},
        {"$set": {
            "nom_prenom": nom_prenom,
            "age": age,
            "classe": classe,
            "moyenne": moyenne
        }}
    )


def supprimer_etudiant(etudiant_id):
    collection.delete_one({"_id": ObjectId(etudiant_id)})


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #f0f2f5;
        --bg-secondary: #ffffff;
        --bg-sidebar: #1a1d23;
        --text-primary: #1a1d23;
        --text-secondary: #6b7280;
        --accent: #2563eb;
        --accent-hover: #1d4ed8;
        --accent-light: rgba(37, 99, 235, 0.08);
        --success: #059669;
        --success-light: rgba(5, 150, 105, 0.08);
        --danger: #dc2626;
        --danger-light: rgba(220, 38, 38, 0.08);
        --warning: #d97706;
        --border: #e5e7eb;
        --border-focus: #2563eb;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
        --radius: 10px;
    }

    .stApp {
        background-color: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stApp > header { background: transparent !important; }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px !important;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }

    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; }

    [data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > label {
        color: rgba(255,255,255,0.7) !important;
        padding: 10px 16px !important;
        border-radius: var(--radius) !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > label:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stRadio > div > div > div[data-checked="true"] > label {
        background: var(--accent) !important;
        color: white !important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 10px 14px !important;
        font-size: 0.92rem !important;
        transition: all 0.15s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 3px var(--accent-light) !important;
    }

    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }

    .stButton > button {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all 0.15s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: var(--accent-hover) !important;
    }

    div[data-testid="stForm"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 2rem !important;
        box-shadow: var(--shadow-md) !important;
    }

    .stRadio > div {
        background: var(--bg-secondary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 4px !important;
    }

    .stRadio > div > div > label {
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 500 !important;
    }

    .stRadio > div > div > div[data-checked="true"] > label {
        background: var(--accent) !important;
        color: white !important;
    }

    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-md) !important;
        border: 1px solid var(--border) !important;
    }

    [data-testid="stDataFrame"] th {
        background: #f8fafc !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.06em !important;
        color: var(--text-secondary) !important;
        padding: 12px 16px !important;
        border-bottom: 1.5px solid var(--border) !important;
    }

    [data-testid="stDataFrame"] td {
        padding: 12px 16px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stDataFrame"] tr:hover td {
        background: #f8fafc !important;
    }

    .stSuccess {
        background: var(--success-light) !important;
        border: 1px solid rgba(5, 150, 105, 0.2) !important;
        border-radius: var(--radius) !important;
        color: var(--success) !important;
    }

    .stError {
        background: var(--danger-light) !important;
        border: 1px solid rgba(220, 38, 38, 0.2) !important;
        border-radius: var(--radius) !important;
        color: var(--danger) !important;
    }

    .stInfo {
        background: var(--accent-light) !important;
        border: 1px solid rgba(37, 99, 235, 0.15) !important;
        border-radius: var(--radius) !important;
        color: var(--accent) !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
        margin-bottom: 4px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stSelectbox input,
    .stTextArea textarea {
        color: var(--text-primary) !important;
    }

    div[data-testid="stMetric"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: var(--shadow-sm) !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🎓 Gestion Étudiants")
    st.markdown('<p style="color: rgba(255,255,255,0.5); font-size: 0.82rem; margin-top: -8px;">Système de gestion scolaire</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.metric("Étudiants", collection.count_documents({}))

page = st.radio("Navigation", ["Liste", "Ajouter", "Modifier"], horizontal=True, label_visibility="collapsed")

if page == "Liste":
    st.markdown("# 📋 Liste des Étudiants")

    terme = st.text_input("Rechercher", placeholder="Rechercher par numéro, nom ou classe...", label_visibility="collapsed")
    etudiants = rechercher_etudiants(terme)

    if etudiants:
        import pandas as pd
        df = pd.DataFrame(etudiants)
        df = df[["numero", "nom_prenom", "age", "classe", "moyenne"]].rename(columns={
            "numero": "N° Inscription", "nom_prenom": "Nom & Prénom", "age": "Âge", "classe": "Classe", "moyenne": "Moyenne"
        })
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True, hide_index=False)

        st.markdown("---")

        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            selected_numero = st.selectbox("Sélectionner un étudiant", [e.get("numero", "") for e in etudiants])
        with col2:
            if st.button("✏️ Modifier", use_container_width=True):
                etudiant_choisi = next((e for e in etudiants if e.get("numero") == selected_numero), None)
                if etudiant_choisi:
                    st.session_state.editing_id = str(etudiant_choisi["_id"])
                    st.session_state.page = "Modifier"
                    st.rerun()
        with col3:
            if st.button("🗑️ Supprimer", type="primary", use_container_width=True):
                etudiant_choisi = next((e for e in etudiants if e.get("numero") == selected_numero), None)
                if etudiant_choisi:
                    supprimer_etudiant(etudiant_choisi["_id"])
                    st.success(f"{etudiant_choisi.get('nom_prenom', '')} supprimé.")
                    st.rerun()
    else:
        st.info("Aucun étudiant trouvé.")

elif page == "Ajouter":
    st.markdown("# ➕ Nouvel Étudiant")

    nouveau_numero = generer_numero()
    st.info(f"Numéro d'inscription automatique : **{nouveau_numero}**")

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Numéro d'inscription", value=nouveau_numero, disabled=True, key="auto_num")
            nom_prenom = st.text_input("Nom & Prénom *", placeholder="Ex: Dupont Jean")
        with col2:
            age = st.number_input("Âge *", min_value=10, max_value=100, value=18)
            classe = st.selectbox("Classe *", ["", "1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"])

        moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=10.0, step=0.01, format="%.2f")

        submitted = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)

        if submitted:
            if not nom_prenom or not classe:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                inserer_etudiant(nouveau_numero, nom_prenom, age, classe, moyenne)
                st.success(f"{nom_prenom} ajouté avec succès ! ({nouveau_numero})")
                st.balloons()

elif page == "Modifier":
    etudiant_id = st.session_state.get("editing_id")
    etudiant = collection.find_one({"_id": ObjectId(etudiant_id)}) if etudiant_id else None

    if not etudiant:
        st.markdown("# ⚠️ Aucun étudiant sélectionné")
        st.info("Retournez à la liste et cliquez sur **Modifier** pour un étudiant.")
    else:
        st.markdown(f"# ✏️ {etudiant.get('nom_prenom', '')}")
        st.caption(f"Inscrit sous le numéro : **{etudiant.get('numero', '')}**")

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Numéro d'inscription", value=etudiant.get("numero", ""), disabled=True)
                nom_prenom = st.text_input("Nom & Prénom *", value=etudiant.get("nom_prenom", ""))
            with col2:
                age = st.number_input("Âge *", min_value=10, max_value=100, value=etudiant.get("age", 18))
                classes_list = ["1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"]
                current_class = etudiant.get("classe", "")
                classe = st.selectbox("Classe *", classes_list, index=classes_list.index(current_class) if current_class in classes_list else 0)

            moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=float(etudiant.get("moyenne", 10.0)), step=0.01, format="%.2f")

            submitted = st.form_submit_button("💾 Enregistrer les modifications", type="primary", use_container_width=True)

            if submitted:
                if not nom_prenom or not classe:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    modifier_etudiant(etudiant_id, nom_prenom, age, classe, moyenne)
                    st.success(f"{nom_prenom} modifié !")
                    st.session_state.pop("editing_id", None)
                    st.rerun()
