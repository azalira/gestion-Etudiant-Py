# 🎓 Gestion des Etudiants

Application web de gestion des étudiants construite avec **Streamlit** et **MongoDB**.

## 🚀 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer MongoDB

Copiez le fichier d'environnement :

```bash
cp .env.example .env
```

Modifiez `MONGO_URI` si votre MongoDB n'est pas en local.

### 3. Lancer l'application

```bash
streamlit run app.py
```

L'app sera disponible sur `http://localhost:8501`

## 📋 Fonctionnalités

- **Liste des étudiants** avec tableau de bord et statistiques
- **Ajout** d'étudiants avec validation
- **Modification** des informations
- **Suppression** avec confirmation
- **Recherche** par numéro, nom ou classe
- **Filtrage** par classe

## 📊 Champs

| Champ | Type | Description |
|-------|------|-------------|
| Numéro | Texte | Numéro d'inscription unique |
| Nom & Prénom | Texte | Nom complet |
| Âge | Nombre | Âge de l'étudiant |
| Classe | Liste | Classe affectée |
| Moyenne | Nombre | Moyenne générale (0-20) |

## 🔧 Prérequis

- Python 3.8+
- MongoDB (local ou distant)
# gestion-Etudiant-Py
