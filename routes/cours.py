from flask import Blueprint, request, jsonify

from database import db

from flask_jwt_extended import jwt_required

from models.cours import Cours
from models.departement import Departement


cours_bp = Blueprint(
    "cours",
    __name__,
    url_prefix="/cours"
)


# -------------------------
# GET Tous
# -------------------------

@cours_bp.route("/", methods=["GET"])
@jwt_required()
def get_cours():

    cours = Cours.query.all()

    return jsonify({

        "status": "success",

        "data": [
            c.to_dict()
            for c in cours
        ]

    }), 200


# -------------------------
# GET ID
# -------------------------

@cours_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_cours_by_id(id):

    cours = Cours.query.get(id)

    if not cours:

        return jsonify({

            "status": "error",

            "message": "Cours introuvable"

        }),404

    return jsonify({

        "status":"success",

        "data":cours.to_dict()

    }),200


# -------------------------
# POST
# -------------------------

@cours_bp.route("/", methods=["POST"])
@jwt_required()
def create_cours():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Aucune donnée reçue."
        }), 400

    required_fields = ["code_cours", "nom_cours", "id_departement"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "status": "error",
            "message": f"Les champs suivants sont obligatoires : {', '.join(missing_fields)}."
        }), 400

    departement = Departement.query.get(data["id_departement"])
    if not departement:
        return jsonify({
            "status": "error",
            "message": "Département introuvable."
        }), 404

    cours = Cours(
        code_cours=data["code_cours"],
        nom_cours=data["nom_cours"],
        credit=data.get("credit", 0),
        volume_horaire=data.get("volume_horaire", 0),
        id_departement=data["id_departement"]
    )

    db.session.add(cours)
    db.session.commit()

    return jsonify({

        "status":"success",

        "message":"Cours créé avec succès.",

        "data":cours.to_dict()

    }),201


# -------------------------
# PUT
# -------------------------

@cours_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_cours(id):

    cours = Cours.query.get(id)

    if not cours:

        return jsonify({

            "status":"error",

            "message":"Cours introuvable"

        }),404

    data=request.get_json()

    cours.code_cours=data.get(
        "code_cours",
        cours.code_cours
    )

    cours.nom_cours=data.get(
        "nom_cours",
        cours.nom_cours
    )

    cours.credit=data.get(
        "credit",
        cours.credit
    )

    cours.volume_horaire=data.get(
        "volume_horaire",
        cours.volume_horaire
    )

    cours.id_departement=data.get(
        "id_departement",
        cours.id_departement
    )

    db.session.commit()

    return jsonify({

        "status":"success",

        "message":"Cours modifié avec succès.",

        "data":cours.to_dict()

    }),200


# -------------------------
# DELETE
# -------------------------

@cours_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_cours(id):

    cours = Cours.query.get(id)

    if not cours:

        return jsonify({

            "status":"error",

            "message":"Cours introuvable"

        }),404

    db.session.delete(cours)

    db.session.commit()

    return jsonify({

        "status":"success",

        "message":"Cours supprimé avec succès."

    }),200