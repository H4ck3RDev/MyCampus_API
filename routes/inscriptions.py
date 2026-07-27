from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from database import db
from models.inscription import Inscription
from services.inscription_service import (
    creer_inscription,
    modifier_inscription
)


inscriptions_bp = Blueprint(
    "inscriptions",
    __name__,
    url_prefix="/inscriptions"
)


@inscriptions_bp.route("/", methods=["GET"])
@jwt_required()
def get_inscriptions():
    inscriptions = Inscription.query.all()

    return jsonify({
        "status": "success",
        "data": [inscription.to_dict() for inscription in inscriptions]
    }), 200


@inscriptions_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_inscription(id):
    inscription = Inscription.query.get(id)

    if inscription is None:
        return jsonify({
            "status": "error",
            "message": "Inscription introuvable."
        }), 404

    return jsonify({
        "status": "success",
        "data": inscription.to_dict()
    }), 200


@inscriptions_bp.route("/", methods=["POST"])
@jwt_required()
def create_inscription():
    data = request.get_json()
    resultat, code = creer_inscription(data)
    return jsonify(resultat), code


@inscriptions_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_inscription(id):
    inscription = Inscription.query.get(id)

    if inscription is None:
        return jsonify({
            "status": "error",
            "message": "Inscription introuvable."
        }), 404

    data = request.get_json()
    resultat, code = modifier_inscription(inscription, data)
    return jsonify(resultat), code


@inscriptions_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_inscription(id):
    inscription = Inscription.query.get(id)

    if inscription is None:
        return jsonify({
            "status": "error",
            "message": "Inscription introuvable."
        }), 404

    db.session.delete(inscription)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Inscription supprimée avec succès."
    }), 200