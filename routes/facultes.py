from flask import Blueprint, request, jsonify

from database import db
from models.faculte import Faculte

from flask_jwt_extended import jwt_required


facultes_bp = Blueprint(
    "facultes",
    __name__,
    url_prefix="/facultes"
)


# =====================================
# GET toutes les facultés
# =====================================

@facultes_bp.route("/", methods=["GET"])
@jwt_required()
def get_facultes():

    facultes = Faculte.query.all()

    return jsonify({

        "status": "success",

        "data": [

            faculte.to_dict()

            for faculte in facultes

        ]

    }), 200


# =====================================
# GET une faculté
# =====================================

@facultes_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_faculte(id):

    faculte = Faculte.query.get(id)

    if not faculte:

        return jsonify({

            "status": "error",

            "message": "Faculté introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": faculte.to_dict()

    }), 200


# =====================================
# POST
# =====================================

@facultes_bp.route("/", methods=["POST"])
@jwt_required()
def create_faculte():

    data = request.get_json()

    if not data:

        return jsonify({

            "status": "error",

            "message": "Aucune donnée reçue."

        }), 400

    if not data.get("nom"):

        return jsonify({

            "status": "error",

            "message": "Le nom est obligatoire."

        }), 400

    existe = Faculte.query.filter_by(
        nom=data["nom"]
    ).first()

    if existe:

        return jsonify({

            "status": "error",

            "message": "Cette faculté existe déjà."

        }), 409

    faculte = Faculte(

        nom=data["nom"],

        description=data.get("description")

    )

    db.session.add(faculte)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Faculté créée.",

        "data": faculte.to_dict()

    }), 201


# =====================================
# PUT
# =====================================

@facultes_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_faculte(id):

    faculte = Faculte.query.get(id)

    if not faculte:

        return jsonify({

            "status": "error",

            "message": "Faculté introuvable."

        }), 404

    data = request.get_json()

    faculte.nom = data.get(
        "nom",
        faculte.nom
    )

    faculte.description = data.get(
        "description",
        faculte.description
    )

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Faculté modifiée.",

        "data": faculte.to_dict()

    }), 200


# =====================================
# DELETE
# =====================================

@facultes_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_faculte(id):

    faculte = Faculte.query.get(id)

    if not faculte:

        return jsonify({

            "status": "error",

            "message": "Faculté introuvable."

        }), 404

    db.session.delete(faculte)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Faculté supprimée."

    }), 200