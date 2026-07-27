from database import db

from models.utilisateur import Utilisateur
from models.etudiant import Etudiant
from models.role import Role

from werkzeug.security import generate_password_hash


def creer_etudiant(data):
    """
    Création automatique :

    Utilisateur
            ↓
        Etudiant
    """

    # Vérifier si l'email existe déjà
    utilisateur = Utilisateur.query.filter_by(
        email=data["email"]
    ).first()

    if utilisateur:

        return {
            "status": "error",
            "message": "Cet email existe déjà."
        }, 400

    # Recherche du rôle Etudiant
    role = Role.query.filter_by(
        nom_role="Etudiant"
    ).first()

    if role is None:

        return {
            "status": "error",
            "message": "Le rôle Etudiant est introuvable."
        }, 404

    # Création du compte utilisateur
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

    # Création de l'étudiant
    etudiant = Etudiant(

        matricule=data["matricule"],

        id_utilisateur=utilisateur.id_utilisateur,

        id_promotion=data["id_promotion"]

    )

    db.session.add(etudiant)

    db.session.commit()

    return {

        "status": "success",

        "message": "Etudiant créé avec succès.",

        "data": etudiant.to_dict()

    }, 201