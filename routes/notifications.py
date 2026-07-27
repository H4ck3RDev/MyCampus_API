from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.notification import Notification
from models.utilisateur import Utilisateur

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    try:
        notifications = Notification.query.all()

        return jsonify({
            "status": "success",
            "data": [notification.to_dict() for notification in notifications]
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notifications_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_notification(id):
    try:
        notification = Notification.query.get(id)

        if not notification:
            return jsonify({
                "status": "error",
                "message": "Notification introuvable."
            }), 404

        return jsonify({
            "status": "success",
            "data": notification.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notifications_bp.route("/", methods=["POST"])
@jwt_required()
def create_notification():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        titre = data.get("titre")
        contenu = data.get("contenu")
        id_utilisateur = data.get("id_utilisateur")

        if not titre or not contenu or not id_utilisateur:
            return jsonify({
                "status": "error",
                "message": "Les champs titre, contenu et id_utilisateur sont requis."
            }), 400

        utilisateur = Utilisateur.query.get(id_utilisateur)

        if not utilisateur:
            return jsonify({
                "status": "error",
                "message": "Utilisateur introuvable."
            }), 404

        notification = Notification(
            titre=titre,
            contenu=contenu,
            id_utilisateur=id_utilisateur,
            lu=data.get("lu", False)
        )

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Notification créée.",
            "data": notification.to_dict()
        }), 201
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notifications_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_notification(id):
    try:
        notification = Notification.query.get(id)

        if not notification:
            return jsonify({
                "status": "error",
                "message": "Notification introuvable."
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        notification.titre = data.get("titre", notification.titre)
        notification.contenu = data.get("contenu", notification.contenu)
        notification.id_utilisateur = data.get("id_utilisateur", notification.id_utilisateur)
        notification.lu = data.get("lu", notification.lu)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Notification modifiée.",
            "data": notification.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@notifications_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_notification(id):
    try:
        notification = Notification.query.get(id)

        if not notification:
            return jsonify({
                "status": "error",
                "message": "Notification introuvable."
            }), 404

        db.session.delete(notification)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Notification supprimée avec succès."
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500
