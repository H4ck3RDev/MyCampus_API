from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.etudiant import Etudiant
from services.etudiant_service import creer_etudiant

etudiants_bp = Blueprint(
    "etudiants",
    __name__,
    url_prefix="/etudiants"
)


# ==========================
# GET Tous les étudiants
# ==========================

@etudiants_bp.route("/", methods=["GET"])
@jwt_required()
def get_etudiants():

    etudiants = Etudiant.query.all()

    return jsonify({

        "status": "success",

        "data": [
            etudiant.to_dict()
            for etudiant in etudiants
        ]

    }), 200


# ==========================
# GET Etudiant par ID
# ==========================

@etudiants_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_etudiant(id):

    etudiant = Etudiant.query.get(id)

    if etudiant is None:

        return jsonify({

            "status": "error",

            "message": "Etudiant introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": etudiant.to_dict()

    }), 200


# ==========================
# POST
# ==========================

@etudiants_bp.route("/", methods=["POST"])
@jwt_required()
def create_etudiant():

    data = request.get_json()

    resultat, code = creer_etudiant(data)

    return jsonify(resultat), code