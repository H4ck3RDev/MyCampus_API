from flask import Blueprint, request, jsonify
from database import db
from models.utilisateur import Utilisateur
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required

utilisateurs_bp = Blueprint(
    "utilisateurs",
    __name__,
    url_prefix="/utilisateurs"
)

# GET tous les utilisateurs

@utilisateurs_bp.route("/", methods=["GET"])
@jwt_required()
def get_utilisateurs():

    utilisateurs = Utilisateur.query.all()

    return jsonify({

        "status":"success",
        "data":[
            user.to_dict()
            for user in utilisateurs
        ]

    }),200


# GET utilisateur par ID

@utilisateurs_bp.route(
    "/<int:id>",
    methods=["GET"]
)
@jwt_required()
def get_utilisateur(id):

    user=Utilisateur.query.get(id)

    if not user:
        return jsonify({
            "message":
            "Utilisateur introuvable"
        }),404

    return jsonify(
        user.to_dict()
    ),200


# POST utilisateur

@utilisateurs_bp.route(
    "/",
    methods=["POST"]
)
@jwt_required()
def create_utilisateur():

    data=request.json

    utilisateur=Utilisateur(

        nom=data["nom"],
        postnom=data.get(
            "postnom"
        ),
        prenom=data.get(
            "prenom"
        ),
        email=data["email"],
        telephone=data.get(
            "telephone"
        ),
        mot_de_passe=
        generate_password_hash(
            data["mot_de_passe"]
        ),
        id_role=data["id_role"]

    )

    db.session.add(utilisateur)
    db.session.commit()

    return jsonify({

        "message":
        "Utilisateur créé",

        "data":
        utilisateur.to_dict()

    }),201

@utilisateurs_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_utilisateur(id):

    utilisateur = Utilisateur.query.get(id)

    if not utilisateur:
        return jsonify({
            "status": "error",
            "message": "Utilisateur introuvable"
        }), 404

    data = request.get_json()

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
    utilisateur.statut = data.get(
        "statut",
        utilisateur.statut
    )
    utilisateur.id_role = data.get(
        "id_role",
        utilisateur.id_role
    )

    # Modifier le mot de passe seulement s'il est fourni
    if data.get("mot_de_passe"):
        utilisateur.mot_de_passe = generate_password_hash(
            data["mot_de_passe"]
        )

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Utilisateur modifié avec succès",
        "data": utilisateur.to_dict()
    }), 200

@utilisateurs_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_utilisateur(id):

    utilisateur = Utilisateur.query.get(id)

    if not utilisateur:
        return jsonify({
            "status": "error",
            "message": "Utilisateur introuvable"
        }), 404

    db.session.delete(utilisateur)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Utilisateur supprimé avec succès"
    }), 200