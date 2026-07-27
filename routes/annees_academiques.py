from flask import Blueprint, request, jsonify

from database import db
from models.annee_academique import AnneeAcademique

from flask_jwt_extended import jwt_required


annees_academiques_bp = Blueprint(
    "annees_academiques",
    __name__,
    url_prefix="/annees_academiques"
)


# =====================================
# GET toutes les années académiques
# =====================================

@annees_academiques_bp.route("/", methods=["GET"])
@jwt_required()
def get_annees_academiques():

    annees = AnneeAcademique.query.all()

    return jsonify({

        "status": "success",

        "data": [

            annee.to_dict()

            for annee in annees

        ]

    }), 200


# =====================================
# GET une année académique
# =====================================

@annees_academiques_bp.route(
    "/<int:id>",
    methods=["GET"]
)
@jwt_required()
def get_annee(id):

    annee = AnneeAcademique.query.get(id)

    if not annee:

        return jsonify({

            "status": "error",

            "message": "Année académique introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": annee.to_dict()

    }), 200


# =====================================
# POST
# =====================================

@annees_academiques_bp.route(
    "/",
    methods=["POST"]
)
@jwt_required()
def create_annee():

    data = request.get_json()

    if not data:

        return jsonify({

            "status": "error",

            "message": "Aucune donnée reçue."

        }), 400


    if not data.get("libelle"):

        return jsonify({

            "status": "error",

            "message": "Le libellé est obligatoire."

        }), 400


    existe = AnneeAcademique.query.filter_by(
        libelle=data["libelle"]
    ).first()

    if existe:

        return jsonify({

            "status": "error",

            "message": "Cette année académique existe déjà."

        }), 409


    annee = AnneeAcademique(

        libelle=data["libelle"],

        date_debut=data.get("date_debut"),

        date_fin=data.get("date_fin")

    )

    db.session.add(annee)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Année académique créée.",

        "data": annee.to_dict()

    }), 201


# =====================================
# PUT
# =====================================

@annees_academiques_bp.route(
    "/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def update_annee(id):

    annee = AnneeAcademique.query.get(id)

    if not annee:

        return jsonify({

            "status": "error",

            "message": "Année académique introuvable."

        }), 404


    data = request.get_json()

    annee.libelle = data.get(
        "libelle",
        annee.libelle
    )

    annee.date_debut = data.get(
        "date_debut",
        annee.date_debut
    )

    annee.date_fin = data.get(
        "date_fin",
        annee.date_fin
    )

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Année académique modifiée.",

        "data": annee.to_dict()

    }), 200


# =====================================
# DELETE
# =====================================

@annees_academiques_bp.route(
    "/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_annee(id):

    annee = AnneeAcademique.query.get(id)

    if not annee:

        return jsonify({

            "status": "error",

            "message": "Année académique introuvable."

        }), 404

    db.session.delete(annee)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Année académique supprimée."

    }), 200