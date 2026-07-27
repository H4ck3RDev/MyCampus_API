from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.presence import Presence
from models.etudiant import Etudiant
from models.cours import Cours

presences_bp = Blueprint(
    "presences",
    __name__,
    url_prefix="/presences"
)


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except Exception:
        return None


@presences_bp.route("/", methods=["GET"])
@jwt_required()
def get_presences():
    presences = Presence.query.all()

    return jsonify({
        "status": "success",
        "data": [presence.to_dict() for presence in presences]
    }), 200


@presences_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_presence(id):
    presence = Presence.query.get(id)

    if not presence:
        return jsonify({
            "status": "error",
            "message": "Présence introuvable."
        }), 404

    return jsonify({
        "status": "success",
        "data": presence.to_dict()
    }), 200


@presences_bp.route("/", methods=["POST"])
@jwt_required()
def create_presence():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Aucune donnée reçue."
        }), 400

    id_etudiant = data.get("id_etudiant")
    date_presence = data.get("date_presence")

    if id_etudiant is None or not date_presence:
        return jsonify({
            "status": "error",
            "message": "Les champs id_etudiant et date_presence sont requis."
        }), 400

    etudiant = Etudiant.query.get(id_etudiant)

    if not etudiant:
        return jsonify({
            "status": "error",
            "message": "Étudiant introuvable."
        }), 404

    parsed_date = parse_date(date_presence)
    if not parsed_date:
        return jsonify({
            "status": "error",
            "message": "Le format de date_presence doit être AAAA-MM-JJ."
        }), 400

    cours = None
    if data.get("id_cours") is not None:
        cours = Cours.query.get(data.get("id_cours"))
        if not cours:
            return jsonify({
                "status": "error",
                "message": "Cours introuvable."
            }), 404

    presence = Presence(
        id_etudiant=id_etudiant,
        id_cours=data.get("id_cours"),
        date_presence=parsed_date,
        statut=data.get("statut", "present"),
        commentaire=data.get("commentaire")
    )

    db.session.add(presence)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Présence enregistrée.",
        "data": presence.to_dict()
    }), 201


@presences_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_presence(id):
    presence = Presence.query.get(id)

    if not presence:
        return jsonify({
            "status": "error",
            "message": "Présence introuvable."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Aucune donnée reçue."
        }), 400

    if data.get("id_etudiant") is not None:
        etudiant = Etudiant.query.get(data["id_etudiant"])
        if not etudiant:
            return jsonify({
                "status": "error",
                "message": "Étudiant introuvable."
            }), 404
        presence.id_etudiant = data["id_etudiant"]

    if data.get("id_cours") is not None:
        cours = Cours.query.get(data["id_cours"])
        if not cours:
            return jsonify({
                "status": "error",
                "message": "Cours introuvable."
            }), 404
        presence.id_cours = data["id_cours"]

    if data.get("date_presence"):
        parsed_date = parse_date(data["date_presence"])
        if not parsed_date:
            return jsonify({
                "status": "error",
                "message": "Le format de date_presence doit être AAAA-MM-JJ."
            }), 400
        presence.date_presence = parsed_date

    presence.statut = data.get("statut", presence.statut)
    presence.commentaire = data.get("commentaire", presence.commentaire)

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Présence modifiée.",
        "data": presence.to_dict()
    }), 200


@presences_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_presence(id):
    presence = Presence.query.get(id)

    if not presence:
        return jsonify({
            "status": "error",
            "message": "Présence introuvable."
        }), 404

    db.session.delete(presence)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Présence supprimée avec succès."
    }), 200
