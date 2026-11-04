
# ============================================================
# Application de consultation des notes des étudiants
# ============================================================

import os
import sqlite3

from flask import Flask, jsonify, request
from auth import utilisateur_connecte

app = Flask(__name__)

# Base de données
DB = "notes.db"


# ============================================================
# Initialisation de la base de données
# ============================================================

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, "
            "etudiant TEXT, module TEXT, note REAL)"
        )

        if con.execute(
            "SELECT COUNT(*) FROM notes"
        ).fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes "
                "(etudiant, module, note) VALUES (?, ?, ?)",
                [
                    ("Amina", "DevSecOps", 15.5),
                    ("Youssef", "DevSecOps", 12.0),
                ],
            )


init_db()


# ============================================================
# Page d'accueil
# ============================================================

@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'>"
        "<head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head>"
        "<body><h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p>"
        "</body></html>"
    )


# ============================================================
# Vérification du service
# ============================================================


@app.route("/health")
def health():
    return jsonify(status="ok", version="1.0")



# ============================================================
# Consultation et recherche des notes
# ============================================================

@app.route("/notes")
def lister_notes():
    etudiant = request.args.get("etudiant", "")

    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note "
            "FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",),
        ).fetchall()

    return jsonify([
        {
            "id": r[0],
            "etudiant": r[1],
            "module": r[2],
            "note": r[3],
        }
        for r in rows
    ])


# ============================================================
# Modification sécurisée d'une note
# ============================================================

@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):

    # S2 : Vérifier l'authentification
    utilisateur = utilisateur_connecte()

    if utilisateur is None:
        return "Authentification requise", 401

    # S3 : Vérifier le rôle
    if utilisateur.get("role") != "enseignant":
        return "Accès interdit", 403

    # S5 : Vérifier la nouvelle note
    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return "Données invalides", 400

    nouvelle_note = donnees.get("note")

    if (
        isinstance(nouvelle_note, bool)
        or not isinstance(nouvelle_note, (int, float))
        or not 0 <= nouvelle_note <= 20
    ):
        return "Note invalide", 400

    try:
        with sqlite3.connect(DB) as con:

            # S4 : Vérifier le module
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,),
            ).fetchone()

            if resultat is None:
                return "Note introuvable", 404

            if utilisateur.get("module") != resultat[0]:
                return "Accès interdit", 403

            # S6 : Modifier la note avec SQL paramétré
            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (nouvelle_note, note_id),
            )

        return "OK", 200

    # S7 : Ne pas divulguer les erreurs techniques
    except sqlite3.Error:
        app.logger.error(
            "Erreur de base de données pendant "
            "la modification d'une note"
        )
        return "Erreur interne du serveur", 500


# ============================================================
# Démarrage du service des notes
# ============================================================

if __name__ == "__main__":
    app.run(
        host=os.environ.get("APP_HOST", "127.0.0.1"),
        port=5000,
    )
