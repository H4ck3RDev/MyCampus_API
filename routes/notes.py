from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.cours import Cours
from models.etudiant import Etudiant
from models.professeur import Professeur
from models.note import Note

notes_bp = Blueprint(
    "notes",
    __name__,
    url_prefix="/notes"
)


@notes_bp.route("/", methods=["GET"])
@jwt_required()
def get_notes():
    try:
        notes = Note.query.all()

        return jsonify({
            "status": "success",
            "data": [note.to_dict() for note in notes]
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notes_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_note(id):
    try:
        note = Note.query.get(id)

        if not note:
            return jsonify({
                "status": "error",
                "message": "Note introuvable."
            }), 404

        return jsonify({
            "status": "success",
            "data": note.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notes_bp.route("/", methods=["POST"])
@jwt_required()
def create_note():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        valeur = data.get("valeur")
        id_etudiant = data.get("id_etudiant")
        id_cours = data.get("id_cours")

        if valeur is None or id_etudiant is None or id_cours is None:
            return jsonify({
                "status": "error",
                "message": "Les champs valeur, id_etudiant et id_cours sont requis."
            }), 400

        etudiant = Etudiant.query.get(id_etudiant)
        cours = Cours.query.get(id_cours)

        if not etudiant:
            return jsonify({
                "status": "error",
                "message": "Étudiant introuvable."
            }), 404

        if not cours:
            return jsonify({
                "status": "error",
                "message": "Cours introuvable."
            }), 404

        note = Note(
            valeur=valeur,
            type_note=data.get("type_note"),
            commentaire=data.get("commentaire"),
            id_etudiant=id_etudiant,
            id_cours=id_cours,
            id_professeur=data.get("id_professeur")
        )

        db.session.add(note)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Note créée.",
            "data": note.to_dict()
        }), 201
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notes_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_note(id):
    try:
        note = Note.query.get(id)

        if not note:
            return jsonify({
                "status": "error",
                "message": "Note introuvable."
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        if data.get("id_etudiant"):
            etudiant = Etudiant.query.get(data["id_etudiant"])
            if not etudiant:
                return jsonify({
                    "status": "error",
                    "message": "Étudiant introuvable."
                }), 404
            note.id_etudiant = data["id_etudiant"]

        if data.get("id_cours"):
            cours = Cours.query.get(data["id_cours"])
            if not cours:
                return jsonify({
                    "status": "error",
                    "message": "Cours introuvable."
                }), 404
            note.id_cours = data["id_cours"]

        note.valeur = data.get("valeur", note.valeur)
        note.type_note = data.get("type_note", note.type_note)
        note.commentaire = data.get("commentaire", note.commentaire)
        note.id_professeur = data.get("id_professeur", note.id_professeur)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Note modifiée.",
            "data": note.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notes_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):
    try:
        note = Note.query.get(id)

        if not note:
            return jsonify({
                "status": "error",
                "message": "Note introuvable."
            }), 404

        db.session.delete(note)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Note supprimée avec succès."
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500
