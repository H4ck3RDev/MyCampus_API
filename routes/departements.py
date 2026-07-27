from flask import Blueprint, request, jsonify

from database import db

from models.departement import Departement
from models.faculte import Faculte

from flask_jwt_extended import jwt_required


departements_bp = Blueprint(
    "departements",
    __name__,
    url_prefix="/departements"
)


# =====================================
# GET tous les départements
# =====================================

@departements_bp.route("/", methods=["GET"])
@jwt_required()
def get_departements():

    departements = Departement.query.all()

    return jsonify({

        "status": "success",

        "data": [
            departement.to_dict()
            for departement in departements
        ]

    }), 200


# =====================================
# GET département par ID
# =====================================

@departements_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_departement(id):

    departement = Departement.query.get(id)

    if not departement:

        return jsonify({

            "status": "error",

            "message": "Département introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": departement.to_dict()

    }), 200


# =====================================
# POST
# =====================================

@departements_bp.route("/", methods=["POST"])
@jwt_required()
def create_departement():

    data = request.get_json()

    if not data:

        return jsonify({

            "status": "error",

            "message": "Aucune donnée reçue."

        }), 400

    if not data.get("nom"):

        return jsonify({

            "status": "error",

            "message": "Le nom du département est obligatoire."

        }), 400

    if not data.get("id_faculte"):

        return jsonify({

            "status": "error",

            "message": "La faculté est obligatoire."

        }), 400

    faculte = Faculte.query.get(data["id_faculte"])

    if not faculte:

        return jsonify({

            "status": "error",

            "message": "La faculté n'existe pas."

        }), 404

    departement = Departement(

        nom=data["nom"],

        description=data.get("description"),

        id_faculte=data["id_faculte"]

    )

    db.session.add(departement)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Département créé.",

        "data": departement.to_dict()

    }), 201


# =====================================
# PUT
# =====================================

@departements_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_departement(id):

    departement = Departement.query.get(id)

    if not departement:

        return jsonify({

            "status": "error",

            "message": "Département introuvable."

        }), 404

    data = request.get_json()

    departement.nom = data.get(
        "nom",
        departement.nom
    )

    departement.description = data.get(
        "description",
        departement.description
    )

    if data.get("id_faculte"):

        faculte = Faculte.query.get(data["id_faculte"])

        if not faculte:

            return jsonify({

                "status": "error",

                "message": "La faculté n'existe pas."

            }), 404

        departement.id_faculte = data["id_faculte"]

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Département modifié.",

        "data": departement.to_dict()

    }), 200


# =====================================
# DELETE
# =====================================

@departements_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_departement(id):

    departement = Departement.query.get(id)

    if not departement:

        return jsonify({

            "status": "error",

            "message": "Département introuvable."

        }), 404

    db.session.delete(departement)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Département supprimé."

    }), 200