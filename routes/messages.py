from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.message import Message
from models.utilisateur import Utilisateur

messages_bp = Blueprint(
    "messages",
    __name__,
    url_prefix="/messages"
)


@messages_bp.route("/", methods=["GET"])
@jwt_required()
def get_messages():
    try:
        messages = Message.query.all()

        return jsonify({
            "status": "success",
            "data": [message.to_dict() for message in messages]
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@messages_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_message(id):
    try:
        message = Message.query.get(id)

        if not message:
            return jsonify({
                "status": "error",
                "message": "Message introuvable."
            }), 404

        return jsonify({
            "status": "success",
            "data": message.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@messages_bp.route("/", methods=["POST"])
@jwt_required()
def create_message():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        sujet = data.get("sujet")
        contenu = data.get("contenu")
        id_expediteur = data.get("id_expediteur")
        id_destinataire = data.get("id_destinataire")

        if not sujet or not contenu or not id_expediteur or not id_destinataire:
            return jsonify({
                "status": "error",
                "message": "Les champs sujet, contenu, id_expediteur et id_destinataire sont requis."
            }), 400

        expediteur = Utilisateur.query.get(id_expediteur)
        destinataire = Utilisateur.query.get(id_destinataire)

        if not expediteur or not destinataire:
            return jsonify({
                "status": "error",
                "message": "Expéditeur ou destinataire introuvable."
            }), 404

        message = Message(
            sujet=sujet,
            contenu=contenu,
            id_expediteur=id_expediteur,
            id_destinataire=id_destinataire,
            statut=data.get("statut", "envoyé")
        )

        db.session.add(message)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Message envoyé.",
            "data": message.to_dict()
        }), 201
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@messages_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_message(id):
    try:
        message = Message.query.get(id)

        if not message:
            return jsonify({
                "status": "error",
                "message": "Message introuvable."
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        message.sujet = data.get("sujet", message.sujet)
        message.contenu = data.get("contenu", message.contenu)
        message.id_expediteur = data.get("id_expediteur", message.id_expediteur)
        message.id_destinataire = data.get("id_destinataire", message.id_destinataire)
        message.statut = data.get("statut", message.statut)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Message modifié.",
            "data": message.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@messages_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_message(id):
    try:
        message = Message.query.get(id)

        if not message:
            return jsonify({
                "status": "error",
                "message": "Message introuvable."
            }), 404

        db.session.delete(message)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Message supprimé avec succès."
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500
