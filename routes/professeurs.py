from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.professeur import Professeur
from services.professeur_service import creer_professeur

professeurs_bp = Blueprint(
    "professeurs",
    __name__,
    url_prefix="/professeurs"
)


# ==========================
# GET Tous les professeurs
# ==========================

@professeurs_bp.route("/", methods=["GET"])
@jwt_required()
def get_professeurs():

    professeurs = Professeur.query.all()

    return jsonify({

        "status": "success",

        "data": [
            professeur.to_dict()
            for professeur in professeurs
        ]

    }), 200


# ==========================
# GET Professeur par ID
# ==========================

@professeurs_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_professeur(id):

    professeur = Professeur.query.get(id)

    if professeur is None:

        return jsonify({

            "status": "error",

            "message": "Professeur introuvable."

        }), 404

    return jsonify({

        "status": "success",

        "data": professeur.to_dict()

    }), 200


# ==========================
# POST Professeur
# ==========================

@professeurs_bp.route("/", methods=["POST"])
@jwt_required()
def create_professeur():

    data = request.get_json()

    resultat, code = creer_professeur(data)

    return jsonify(resultat), code


# ==========================
# PUT Professeur
# ==========================

@professeurs_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_professeur(id):

    professeur = Professeur.query.get(id)

    if professeur is None:
        return jsonify({
            "status": "error",
            "message": "Professeur introuvable."
        }), 404

    data = request.get_json()

    utilisateur = professeur.utilisateur

    utilisateur.nom = data.get("nom", utilisateur.nom)
    utilisateur.postnom = data.get("postnom", utilisateur.postnom)
    utilisateur.prenom = data.get("prenom", utilisateur.prenom)
    utilisateur.sexe = data.get("sexe", utilisateur.sexe)
    utilisateur.date_naissance = data.get(
        "date_naissance",
        utilisateur.date_naissance
    )
    utilisateur.telephone = data.get(
        "telephone",
        utilisateur.telephone
    )
    utilisateur.email = data.get(
        "email",
        utilisateur.email
    )
    utilisateur.photo = data.get(
        "photo",
        utilisateur.photo
    )

    professeur.grade = data.get(
        "grade",
        professeur.grade
    )

    professeur.specialite = data.get(
        "specialite",
        professeur.specialite
    )

    from database import db
    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Professeur modifié avec succès.",

        "data": professeur.to_dict()

    }), 200


# ==========================
# DELETE Professeur
# ==========================

@professeurs_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_professeur(id):

    professeur = Professeur.query.get(id)

    if professeur is None:

        return jsonify({

            "status": "error",

            "message": "Professeur introuvable."

        }), 404

    from database import db

    utilisateur = professeur.utilisateur

    db.session.delete(professeur)

    if utilisateur:
        db.session.delete(utilisateur)

    db.session.commit()

    return jsonify({

        "status": "success",

        "message": "Professeur supprimé avec succès."

    }), 200