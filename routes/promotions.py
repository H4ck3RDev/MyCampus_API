from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from database import db

from models.promotion import Promotion
from models.departement import Departement


promotions_bp = Blueprint(
    "promotions",
    __name__,
    url_prefix="/promotions"
)


# =====================================
# GET toutes les promotions
# =====================================

@promotions_bp.route("/", methods=["GET"])
@jwt_required()
def get_promotions():

    promotions = Promotion.query.all()

    return jsonify({

        "status": "success",

        "data": [

            promotion.to_dict()

            for promotion in promotions

        ]

    }), 200


# =====================================
# GET promotion par ID
# =====================================

@promotions_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_promotion(id):

    promotion = Promotion.query.get(id)

    if not promotion:

        return jsonify({

            "status": "error",

            "message": "Promotion introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": promotion.to_dict()

    }), 200


# =====================================
# POST
# =====================================

@promotions_bp.route("/", methods=["POST"])
@jwt_required()
def create_promotion():

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

    if not data.get("id_departement"):

        return jsonify({

            "status": "error",

            "message": "Le département est obligatoire."

        }), 400

    departement = Departement.query.get(
        data["id_departement"]
    )

    if not departement:

        return jsonify({

            "status": "error",

            "message": "Département introuvable."

        }), 404

    promotion = Promotion(

        nom=data["nom"],

        niveau=data.get("niveau"),

        id_departement=data["id_departement"]

    )

    db.session.add(promotion)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Promotion créée.",

        "data": promotion.to_dict()

    }), 201


# =====================================
# PUT
# =====================================

@promotions_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_promotion(id):

    promotion = Promotion.query.get(id)

    if not promotion:

        return jsonify({

            "status": "error",

            "message": "Promotion introuvable."

        }), 404

    data = request.get_json()

    promotion.nom = data.get(
        "nom",
        promotion.nom
    )

    promotion.niveau = data.get(
        "niveau",
        promotion.niveau
    )

    if data.get("id_departement"):

        departement = Departement.query.get(
            data["id_departement"]
        )

        if not departement:

            return jsonify({

                "status": "error",

                "message": "Département introuvable."

            }), 404

        promotion.id_departement = data["id_departement"]

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Promotion modifiée.",

        "data": promotion.to_dict()

    }), 200


# =====================================
# DELETE
# =====================================

@promotions_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_promotion(id):

    promotion = Promotion.query.get(id)

    if not promotion:

        return jsonify({

            "status": "error",

            "message": "Promotion introuvable."

        }), 404

    db.session.delete(promotion)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Promotion supprimée."

    }), 200