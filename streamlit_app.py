import streamlit as st
from db import compter, lister, trouver, ajouter, modifier, supprimer

st.set_page_config(page_title="Gestion des Etudiants", page_icon="🎓", layout="wide")


def generer_numero():
    count = compter()
    return f"ETU-{str(count + 1).zfill(4)}"


st.markdown(
    """
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
    .stApp { background: var(--bg) !important; font-family: 'Inter', sans-serif !important; transition: background 0.2s ease !important; }
    .stApp > header { background: transparent !important; }
    .main .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1100px !important; animation: fadeIn 0.3s ease !important; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: var(--text) !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
    [data-testid="stSidebar"] { background: var(--sidebar-bg) !important; transition: background 0.2s ease !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #fff !important; }
    [data-testid="stSidebar"] .stRadio > div { background: transparent !important; border: none !important; }
    [data-testid="stSidebar"] .stRadio > div > div > label { color: rgba(255,255,255,0.7) !important; padding: 10px 16px !important; border-radius: var(--radius) !important; }
    [data-testid="stSidebar"] .stRadio > div > div > label:hover { background: rgba(255,255,255,0.08) !important; color: #fff !important; }
    [data-testid="stSidebar"] .stRadio > div > div > div[data-checked="true"] > label { background: var(--accent) !important; color: white !important; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: var(--card) !important; color: var(--text) !important;
        border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important;
        padding: 10px 14px !important; font-size: 0.92rem !important; font-family: 'Inter', sans-serif !important; width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: var(--border-focus) !important; box-shadow: 0 0 0 3px var(--accent-bg) !important;
        outline: none !important;
    }
    .stSelectbox > div > div { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; transition: all 0.2s ease !important; }
    .stButton > button { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; padding: 8px 20px !important; font-weight: 500 !important; font-size: 0.88rem !important; font-family: 'Inter', sans-serif !important; width: 100% !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; transform: translateY(-1px) !important; }
    .stButton > button:active { transform: translateY(0) !important; }
    .stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button { background: var(--accent) !important; color: white !important; border: none !important; font-weight: 600 !important; }
    .stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] > button:hover { background: var(--accent-hover) !important; transform: translateY(-1px) !important; }
    div[data-testid="stForm"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; padding: 2rem 2.5rem !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07) !important; transition: all 0.3s ease !important; }
    .stRadio > div { background: #000000 !important; border: 1.5px solid #000000 !important; border-radius: var(--radius) !important; padding: 4px !important; }
    .stRadio > div > div > label { border-radius: 8px !important; padding: 8px 18px !important; font-weight: 500 !important; color: #000000 !important; transition: all 0.2s ease !important; }
    .stRadio > div > div > div[data-checked="true"] > label { background: var(--accent) !important; color: white !important; }
    .stRadio label { color: #000000 !important; }
    .stRadio span { color: #000000 !important; }
    .stRadio div[data-checked="true"] span { color: white !important; }
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07) !important; border: 1px solid var(--border) !important; transition: all 0.2s ease !important; }
    [data-testid="stDataFrame"] th { background: #f8fafc !important; font-weight: 600 !important; text-transform: uppercase !important; font-size: 0.72rem !important; letter-spacing: 0.06em !important; color: var(--text-muted) !important; padding: 12px 16px !important; border-bottom: 1.5px solid var(--border) !important; }
    [data-testid="stDataFrame"] td { padding: 12px 16px !important; border-bottom: 1px solid #f1f5f9 !important; font-size: 0.9rem !important; color: var(--text) !important; transition: background 0.15s ease !important; }
    [data-testid="stDataFrame"] tr:hover td { background: #f8fafc !important; }
    [data-testid="stDataFrame"] [data-testid="stDataFrameCell"] { color: var(--text) !important; }
    [data-testid="stDataFrame"] div { color: var(--text) !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label { font-weight: 500 !important; color: var(--text) !important; font-size: 0.82rem !important; margin-bottom: 2px !important; font-family: 'Inter', sans-serif !important; white-space: nowrap !important; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input { color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; caret-color: #000000 !important; }
    .stTextInput > div > div > input::placeholder { -webkit-text-fill-color: var(--text-muted) !important; }
    .stTextInput > div > div > input:disabled, .stNumberInput > div > div > input:disabled { background: #f8fafc !important; color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; border-color: var(--border) !important; }
    .stAlert > div { color: #000000 !important; }
    .stAlert p { color: #000000 !important; }
    .stAlert div[data-testid="stMarkdownContainer"] { color: #000000 !important; }
    div[data-testid="stMetric"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 20px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important; }
    [data-testid="stSidebar"] div[data-testid="stMetric"] { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.12) !important; }
    [data-testid="stSidebar"] div[data-testid="stMetric"] label { color: rgba(255,255,255,0.6) !important; }
    [data-testid="stSidebar"] div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #ffffff !important; }
    .form-note { font-size: 0.8rem; color: var(--text-muted); margin-top: 8px; }
</style>
<script>
document.addEventListener('DOMContentLoaded', function() {
    function setCursorToEnd() {
        document.querySelectorAll('input[type="text"], input:not([type])').forEach(function(input) {
            if (input.value && !input.disabled) {
                input.focus();
                input.setSelectionRange(input.value.length, input.value.length);
            }
        });
    }
    setTimeout(setCursorToEnd, 500);
    new MutationObserver(setCursorToEnd).observe(document.body, { childList: true, subtree: true });
});
</script>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("# 🎓 Gestion Étudiants")
    st.markdown(
        '<p style="color: rgba(255,255,255,0.5); font-size: 0.82rem; margin-top: -8px;">Système de gestion scolaire</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.metric("Étudiants", compter())

if "page" not in st.session_state:
    st.session_state.page = "Liste"

page = st.radio(
    "Navigation",
    ["Liste", "Ajouter", "Modifier"],
    horizontal=True,
    label_visibility="collapsed",
    index=["Liste", "Ajouter", "Modifier"].index(st.session_state.page),
)
if page != st.session_state.page:
    st.session_state.page = page

if page == "Liste":
    st.markdown("# 📋 Liste des Étudiants")
    terme = st.text_input(
        "Rechercher",
        placeholder="Rechercher par numéro, nom ou classe...",
        label_visibility="collapsed",
    )
    etudiants = lister(terme)

    if etudiants:
        import pandas as pd

        df = pd.DataFrame(etudiants)
        df = df[["numero", "nom_prenom", "age", "classe", "moyenne"]].rename(
            columns={
                "numero": "N° Inscription",
                "nom_prenom": "Nom & Prénom",
                "age": "Âge",
                "classe": "Classe",
                "moyenne": "Moyenne",
            }
        )
        df.index = range(1, len(df) + 1)

        event = st.dataframe(df, use_container_width=True, hide_index=False, on_select="rerun")

        if event and event.selection and event.selection.rows:
            selected_idx = event.selection.rows[0]
            selected_etudiant = etudiants[selected_idx]
            st.session_state.editing_id = selected_etudiant["_id"]
            st.session_state.page = "Modifier"
            st.rerun()

        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            selected_numero = st.selectbox(
                "Sélectionner un étudiant", [e.get("numero", "") for e in etudiants]
            )
        with col2:
            if st.button("✏️ Modifier", use_container_width=True):
                etudiant_choisi = next(
                    (e for e in etudiants if e.get("numero") == selected_numero), None
                )
                if etudiant_choisi:
                    st.session_state.editing_id = etudiant_choisi["_id"]
                    st.session_state.page = "Modifier"
                    st.rerun()
        col_del1, col_del2 = st.columns([1, 1])
        with col_del2:
            if st.button("🗑️ Supprimer", type="primary", use_container_width=True):
                etudiant_choisi = next(
                    (e for e in etudiants if e.get("numero") == selected_numero), None
                )
                if etudiant_choisi:
                    supprimer(etudiant_choisi["_id"])
                    st.success(f"{etudiant_choisi.get('nom_prenom', '')} supprimé.")
                    st.rerun()
    else:
        st.info("Aucun étudiant trouvé.")

elif page == "Ajouter":
    st.markdown("# ➕ Nouvel Étudiant")
    st.markdown(
        '<p style="color: #6b7280; margin-top: -12px; font-size: 0.9rem;">Remplissez les informations ci-dessous</p>',
        unsafe_allow_html=True,
    )
    nouveau_numero = generer_numero()

    with st.form("add_form", clear_on_submit=True):
        st.text_input("N° Inscription", value=nouveau_numero, disabled=True, key="auto_num")
        col1, col2 = st.columns(2)
        with col1:
            nom_prenom = st.text_input("Nom & Prénom *", placeholder="Ex: Dupont Jean")
            age = st.text_input("Âge *", value="18", placeholder="Ex: 20")
        with col2:
            classe = st.selectbox(
                "Classe *",
                ["", "L1", "L2", "L3", "M1", "M2"],
            )
            moyenne = st.text_input("Moyenne *", value="10.00", placeholder="Ex: 14.50")
        st.markdown(
            '<p class="form-note">* Champs obligatoires</p>', unsafe_allow_html=True
        )
        submitted = st.form_submit_button(
            "💾 Enregistrer", type="primary", use_container_width=True
        )
        if submitted:
            if not nom_prenom or not classe or not age or not moyenne:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                try:
                    age_val = int(age)
                    moyenne_val = float(moyenne)
                except ValueError:
                    st.error("Âge doit être un entier et Moyenne doit être un nombre.")
                else:
                    if age_val < 10 or age_val > 100:
                        st.error("L'âge doit être entre 10 et 100 ans.")
                    elif moyenne_val < 0 or moyenne_val > 20:
                        st.error("La moyenne doit être entre 0 et 20.")
                    else:
                        import uuid

                        etudiant = {
                            "_id": str(uuid.uuid4()),
                            "numero": nouveau_numero,
                            "nom_prenom": nom_prenom,
                            "age": age_val,
                            "classe": classe,
                            "moyenne": round(moyenne_val, 2),
                        }
                        ajouter(etudiant)
                        st.success(f"✅ {nom_prenom} ajouté avec succès ! ({nouveau_numero})")
                        st.balloons()

elif page == "Modifier":
    etudiant_id = st.session_state.get("editing_id")
    etudiant = trouver(etudiant_id) if etudiant_id else None

    if not etudiant:
        st.markdown("# ⚠️ Aucun étudiant sélectionné")
        st.markdown('<p style="color: #000000;">Retournez à la liste et cliquez sur <strong>Modifier</strong> pour un étudiant.</p>', unsafe_allow_html=True)
    else:
        st.markdown(f"# ✏️ {etudiant.get('nom_prenom', '')}")
        st.markdown(
            f'<p style="color: #6b7280; margin-top: -12px; font-size: 0.9rem;">N° inscription : <strong>{etudiant.get("numero", "")}</strong></p>',
            unsafe_allow_html=True,
        )

        with st.form("edit_form"):
            st.text_input(
                "N° Inscription", value=etudiant.get("numero", ""), disabled=True
            )
            col1, col2 = st.columns(2)
            with col1:
                nom_prenom = st.text_input(
                    "Nom & Prénom *", value=etudiant.get("nom_prenom", "")
                )
                age = st.text_input(
                    "Âge *", value=str(etudiant.get("age", 18))
                )
            with col2:
                classes_list = ["L1", "L2", "L3", "M1", "M2"]
                current_class = etudiant.get("classe", "")
                classe = st.selectbox(
                    "Classe *",
                    classes_list,
                    index=classes_list.index(current_class)
                    if current_class in classes_list
                    else 0,
                )
                moyenne = st.text_input(
                    "Moyenne *",
                    value=f"{float(etudiant.get('moyenne', 10.0)):.2f}",
                )
            st.markdown(
                '<p class="form-note">* Champs obligatoires</p>', unsafe_allow_html=True
            )
            submitted = st.form_submit_button(
                "💾 Enregistrer les modifications",
                type="primary",
                use_container_width=True,
            )
            if submitted:
                if not nom_prenom or not classe or not age or not moyenne:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    try:
                        age_val = int(age)
                        moyenne_val = float(moyenne)
                    except ValueError:
                        st.error("Âge doit être un entier et Moyenne doit être un nombre.")
                    else:
                        if age_val < 10 or age_val > 100:
                            st.error("L'âge doit être entre 10 et 100 ans.")
                        elif moyenne_val < 0 or moyenne_val > 20:
                            st.error("La moyenne doit être entre 0 et 20.")
                        else:
                            modifier(
                                etudiant_id,
                                {
                                    "nom_prenom": nom_prenom,
                                    "age": age_val,
                                    "classe": classe,
                                    "moyenne": round(moyenne_val, 2),
                                },
                            )
                            st.success(f"✅ {nom_prenom} modifié avec succès !")
                            st.session_state.pop("editing_id", None)
                            st.rerun()
