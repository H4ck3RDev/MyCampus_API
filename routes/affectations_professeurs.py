from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from database import db
from models.affectation_professeur import AffectationProfesseur
from services.affectation_professeur_service import (
    creer_affectation_professeur,
    modifier_affectation_professeur
)


affectations_professeurs_bp = Blueprint(
    "affectations_professeurs",
    __name__,
    url_prefix="/affectations_professeurs"
)


# ==========================
# GET Toutes les affectations
# ==========================

@affectations_professeurs_bp.route("/", methods=["GET"])
@jwt_required()
def get_affectations_professeurs():

    affectations = AffectationProfesseur.query.all()

    return jsonify({
        "status": "success",
        "data": [
            affectation.to_dict()
            for affectation in affectations
        ]
    }), 200


# ==========================
# GET Affectation par ID
# ==========================

@affectations_professeurs_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_affectation_professeur(id):

    affectation = AffectationProfesseur.query.get(id)

    if affectation is None:
        return jsonify({
            "status": "error",
            "message": "Affectation introuvable."
        }), 404

    return jsonify({
        "status": "success",
        "data": affectation.to_dict()
    }), 200


# ==========================
# POST Affectation
# ==========================

@affectations_professeurs_bp.route("/", methods=["POST"])
@jwt_required()
def create_affectation_professeur():

    data = request.get_json()
    resultat, code = creer_affectation_professeur(data)
    return jsonify(resultat), code


# ==========================
# PUT Affectation
# ==========================

@affectations_professeurs_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_affectation_professeur(id):

    affectation = AffectationProfesseur.query.get(id)

    if affectation is None:
        return jsonify({
            "status": "error",
            "message": "Affectation introuvable."
        }), 404

    data = request.get_json()
    resultat, code = modifier_affectation_professeur(affectation, data)
    return jsonify(resultat), code


# ==========================
# DELETE Affectation
# ==========================

@affectations_professeurs_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_affectation_professeur(id):

    affectation = AffectationProfesseur.query.get(id)

    if affectation is None:
        return jsonify({
            "status": "error",
            "message": "Affectation introuvable."
        }), 404

    db.session.delete(affectation)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Affectation professeur supprimée avec succès."
    }), 200