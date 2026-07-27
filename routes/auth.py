from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.utilisateur import Utilisateur

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/", methods=["GET"])
def auth_home():

    return jsonify({
        "status": "success",
        "message": "Module Auth opérationnel."
    }), 200


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Aucune donnée reçue."
        }), 400

    email = data.get("email")
    mot_de_passe = data.get("mot_de_passe")

    if not email or not mot_de_passe:
        return jsonify({
            "status": "error",
            "message": "Email et mot de passe sont obligatoires."
        }), 400

    utilisateur = Utilisateur.query.filter_by(
        email=email
    ).first()

    if utilisateur is None:
        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect."
        }), 401

    if not check_password_hash(
        utilisateur.mot_de_passe,
        mot_de_passe
    ):
        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect."
        }), 401

    if utilisateur.statut != "actif":
        return jsonify({
            "status": "error",
            "message": "Ce compte est désactivé."
        }), 403

    # Génération du JWT
    access_token = create_access_token(
        identity=str(utilisateur.id_utilisateur),
        additional_claims={
            "role": utilisateur.role.nom_role,
            "email": utilisateur.email
        }
    )

    return jsonify({
        "status": "success",
        "message": "Connexion réussie.",
        "access_token": access_token,
        "user": utilisateur.to_dict()
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    return jsonify({
        "status": "success",
        "identity": get_jwt_identity(),
        "claims": get_jwt()
    }), 200