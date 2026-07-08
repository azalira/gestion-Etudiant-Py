import json
import os
from threading import Lock

DB_PATH = os.path.join(os.path.dirname(__file__), "data.json")
_lock = Lock()


def _read():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


def compter():
    with _lock:
        return len(_read())


def lister(terme=""):
    with _lock:
        data = _read()
    if not terme:
        return data
    t = terme.lower()
    return [
        e
        for e in data
        if t in e.get("numero", "").lower()
        or t in e.get("nom_prenom", "").lower()
        or t in e.get("classe", "").lower()
    ]


def trouver(etudiant_id):
    with _lock:
        for e in _read():
            if e["_id"] == etudiant_id:
                return e
    return None


def ajouter(etudiant):
    with _lock:
        data = _read()
        data.append(etudiant)
        _write(data)


def modifier(etudiant_id, updates):
    with _lock:
        data = _read()
        for e in data:
            if e["_id"] == etudiant_id:
                e.update(updates)
                break
        _write(data)


def supprimer(etudiant_id):
    with _lock:
        data = _read()
        data = [e for e in data if e["_id"] != etudiant_id]
        _write(data)
