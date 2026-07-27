from database import db
from werkzeug.security import generate_password_hash

from models.role import Role
from models.utilisateur import Utilisateur
from models.professeur import Professeur


def creer_professeur(data):

    utilisateur = Utilisateur.query.filter_by(
        email=data["email"]
    ).first()

    if utilisateur:
        return {
            "status": "error",
            "message": "Cet email existe déjà."
        }, 400

    role = Role.query.filter_by(
        nom_role="Professeur"
    ).first()

    if role is None:
        return {
            "status": "error",
            "message": "Le rôle Professeur est introuvable."
        }, 404

    utilisateur = Utilisateur(

        nom=data["nom"],

        postnom=data.get("postnom"),

        prenom=data.get("prenom"),

        sexe=data.get("sexe"),

        date_naissance=data.get("date_naissance"),

        telephone=data.get("telephone"),

        email=data["email"],

        mot_de_passe=generate_password_hash(
            data["mot_de_passe"]
        ),

        photo=data.get("photo"),

        id_role=role.id_role

    )

    db.session.add(utilisateur)

    db.session.flush()

    professeur = Professeur(

        grade=data.get("grade"),

        specialite=data.get("specialite"),

        id_utilisateur=utilisateur.id_utilisateur

    )

    db.session.add(professeur)

    db.session.commit()

    return {

        "status": "success",

        "message": "Professeur créé avec succès.",

        "data": professeur.to_dict()

    }, 201