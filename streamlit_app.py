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
    return client[DB_NAME]["etudiants"]


collection = get_db()


def generer_numero():
    count = collection.count_documents({})
    return f"ETU-{str(count + 1).zfill(4)}"


def inserer_etudiant(numero, nom_prenom, age, classe, moyenne):
    return collection.insert_one({
        "numero": numero, "nom_prenom": nom_prenom,
        "age": age, "classe": classe, "moyenne": moyenne
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
        {"$set": {"nom_prenom": nom_prenom, "age": age, "classe": classe, "moyenne": moyenne}}
    )


def supprimer_etudiant(etudiant_id):
    collection.delete_one({"_id": ObjectId(etudiant_id)})


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    :root {
        --bg: #f0f2f5; --card: #ffffff; --sidebar-bg: #1a1d23;
        --text: #1a1d23; --text-muted: #6b7280;
        --accent: #2563eb; --accent-hover: #1d4ed8; --accent-bg: rgba(37,99,235,0.08);
        --green: #059669; --green-bg: rgba(5,150,105,0.08);
        --red: #dc2626; --red-bg: rgba(220,38,38,0.08);
        --border: #e5e7eb; --border-focus: #2563eb; --radius: 10px;
    }
    .stApp { background: var(--bg) !important; font-family: 'Inter', sans-serif !important; }
    .stApp > header { background: transparent !important; }
    .main .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1100px !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: var(--text) !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
    h1 { font-size: 1.7rem !important; }
    [data-testid="stSidebar"] { background: var(--sidebar-bg) !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #fff !important; }
    [data-testid="stSidebar"] .stRadio > div { background: transparent !important; border: none !important; box-shadow: none !important; }
    [data-testid="stSidebar"] .stRadio > div > div > label { color: rgba(255,255,255,0.7) !important; padding: 10px 16px !important; border-radius: var(--radius) !important; }
    [data-testid="stSidebar"] .stRadio > div > div > label:hover { background: rgba(255,255,255,0.08) !important; color: #fff !important; }
    [data-testid="stSidebar"] .stRadio > div > div > div[data-checked="true"] > label { background: var(--accent) !important; color: white !important; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: var(--card) !important; color: var(--text) !important;
        border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important;
        padding: 10px 14px !important; font-size: 0.92rem !important; font-family: 'Inter', sans-serif !important; width: 100% !important;
    }
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: var(--border-focus) !important; box-shadow: 0 0 0 3px var(--accent-bg) !important;
    }
    .stSelectbox > div > div { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; }
    .stButton > button { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; padding: 8px 20px !important; font-weight: 500 !important; font-size: 0.88rem !important; font-family: 'Inter', sans-serif !important; width: 100% !important; }
    .stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
    .stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button { background: var(--accent) !important; color: white !important; border: none !important; font-weight: 600 !important; }
    .stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] > button:hover { background: var(--accent-hover) !important; }
    div[data-testid="stForm"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; padding: 2rem 2.5rem !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07) !important; }
    .stRadio > div { background: var(--card) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; padding: 4px !important; }
    .stRadio > div > div > label { border-radius: 8px !important; padding: 8px 18px !important; font-weight: 500 !important; }
    .stRadio > div > div > div[data-checked="true"] > label { background: var(--accent) !important; color: white !important; }
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07) !important; border: 1px solid var(--border) !important; }
    [data-testid="stDataFrame"] th { background: #f8fafc !important; font-weight: 600 !important; text-transform: uppercase !important; font-size: 0.72rem !important; letter-spacing: 0.06em !important; color: var(--text-muted) !important; padding: 12px 16px !important; border-bottom: 1.5px solid var(--border) !important; }
    [data-testid="stDataFrame"] td { padding: 12px 16px !important; border-bottom: 1px solid #f1f5f9 !important; font-size: 0.9rem !important; }
    [data-testid="stDataFrame"] tr:hover td { background: #f8fafc !important; }
    .stSuccess { background: var(--green-bg) !important; border: 1px solid rgba(5,150,105,0.2) !important; border-radius: var(--radius) !important; color: var(--green) !important; }
    .stError { background: var(--red-bg) !important; border: 1px solid rgba(220,38,38,0.2) !important; border-radius: var(--radius) !important; color: var(--red) !important; }
    .stInfo { background: var(--accent-bg) !important; border: 1px solid rgba(37,99,235,0.15) !important; border-radius: var(--radius) !important; color: var(--accent) !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label { font-weight: 500 !important; color: var(--text) !important; font-size: 0.82rem !important; margin-bottom: 2px !important; font-family: 'Inter', sans-serif !important; white-space: nowrap !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox input, .stTextArea textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    .stTextInput > div > div > input::placeholder { -webkit-text-fill-color: rgba(255,255,255,0.5) !important; }
    div[data-testid="stMetric"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 20px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important; }
    .form-note { font-size: 0.8rem; color: var(--text-muted); margin-top: 8px; }
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
    st.markdown('<p style="color: #6b7280; margin-top: -12px; font-size: 0.9rem;">Remplissez les informations ci-dessous</p>', unsafe_allow_html=True)

    nouveau_numero = generer_numero()

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("N° Inscription", value=nouveau_numero, disabled=True, key="auto_num")
            nom_prenom = st.text_input("Nom & Prénom *", placeholder="Ex: Dupont Jean")
            age = st.number_input("Âge *", min_value=10, max_value=100, value=18)
        with col2:
            classe = st.selectbox("Classe *", ["", "1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"])
            moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=10.0, step=0.01, format="%.2f")
            st.markdown("")

        st.markdown('<p class="form-note">* Champs obligatoires</p>', unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)

        if submitted:
            if not nom_prenom or not classe:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                inserer_etudiant(nouveau_numero, nom_prenom, age, classe, moyenne)
                st.success(f"✅ {nom_prenom} ajouté avec succès ! ({nouveau_numero})")
                st.balloons()

elif page == "Modifier":
    etudiant_id = st.session_state.get("editing_id")
    etudiant = collection.find_one({"_id": ObjectId(etudiant_id)}) if etudiant_id else None

    if not etudiant:
        st.markdown("# ⚠️ Aucun étudiant sélectionné")
        st.info("Retournez à la liste et cliquez sur **Modifier** pour un étudiant.")
    else:
        st.markdown(f"# ✏️ {etudiant.get('nom_prenom', '')}")
        st.markdown(f'<p style="color: #6b7280; margin-top: -12px; font-size: 0.9rem;">N° inscription : <strong>{etudiant.get("numero", "")}</strong></p>', unsafe_allow_html=True)

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("N° Inscription", value=etudiant.get("numero", ""), disabled=True)
                nom_prenom = st.text_input("Nom & Prénom *", value=etudiant.get("nom_prenom", ""))
                age = st.number_input("Âge *", min_value=10, max_value=100, value=etudiant.get("age", 18))
            with col2:
                classes_list = ["1ère Année", "2ème Année", "3ème Année", "L1", "L2", "L3", "M1", "M2"]
                current_class = etudiant.get("classe", "")
                classe = st.selectbox("Classe *", classes_list, index=classes_list.index(current_class) if current_class in classes_list else 0)
                moyenne = st.number_input("Moyenne *", min_value=0.0, max_value=20.0, value=float(etudiant.get("moyenne", 10.0)), step=0.01, format="%.2f")
                st.markdown("")

            st.markdown('<p class="form-note">* Champs obligatoires</p>', unsafe_allow_html=True)
            submitted = st.form_submit_button("💾 Enregistrer les modifications", type="primary", use_container_width=True)

            if submitted:
                if not nom_prenom or not classe:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    modifier_etudiant(etudiant_id, nom_prenom, age, classe, moyenne)
                    st.success(f"✅ {nom_prenom} modifié avec succès !")
                    st.session_state.pop("editing_id", None)
                    st.rerun()
