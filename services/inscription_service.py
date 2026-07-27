from database import db

from models.inscription import Inscription
from models.etudiant import Etudiant
from models.cours import Cours
from models.annee_academique import AnneeAcademique


def creer_inscription(data):
    id_etudiant = data.get("id_etudiant")
    id_cours = data.get("id_cours")
    id_annee = data.get("id_annee")

    if id_etudiant is None or id_cours is None or id_annee is None:
        return {
            "status": "error",
            "message": "Les champs id_etudiant, id_cours et id_annee sont requis."
        }, 400

    etudiant = Etudiant.query.get(id_etudiant)
    if etudiant is None:
        return {
            "status": "error",
            "message": "Étudiant introuvable."
        }, 404

    cours = Cours.query.get(id_cours)
    if cours is None:
        return {
            "status": "error",
            "message": "Cours introuvable."
        }, 404

    annee = AnneeAcademique.query.get(id_annee)
    if annee is None:
        return {
            "status": "error",
            "message": "Année académique introuvable."
        }, 404

    existing = Inscription.query.filter_by(
        id_etudiant=id_etudiant,
        id_cours=id_cours,
        id_annee=id_annee
    ).first()

    if existing is not None:
        return {
            "status": "error",
            "message": "Cette inscription existe déjà."
        }, 400

    inscription = Inscription(
        id_etudiant=id_etudiant,
        id_cours=id_cours,
        id_annee=id_annee
    )

    db.session.add(inscription)
    db.session.commit()

    return {
        "status": "success",
        "message": "Inscription créée avec succès.",
        "data": inscription.to_dict()
    }, 201


def modifier_inscription(inscription, data):
    id_etudiant = data.get("id_etudiant", inscription.id_etudiant)
    id_cours = data.get("id_cours", inscription.id_cours)
    id_annee = data.get("id_annee", inscription.id_annee)

    etudiant = Etudiant.query.get(id_etudiant)
    if etudiant is None:
        return {
            "status": "error",
            "message": "Étudiant introuvable."
        }, 404

    cours = Cours.query.get(id_cours)
    if cours is None:
        return {
            "status": "error",
            "message": "Cours introuvable."
        }, 404

    annee = AnneeAcademique.query.get(id_annee)
    if annee is None:
        return {
            "status": "error",
            "message": "Année académique introuvable."
        }, 404

    existing = Inscription.query.filter(
        Inscription.id_etudiant == id_etudiant,
        Inscription.id_cours == id_cours,
        Inscription.id_annee == id_annee,
        Inscription.id_inscription != inscription.id_inscription
    ).first()

    if existing is not None:
        return {
            "status": "error",
            "message": "Une inscription identique existe déjà."
        }, 400

    inscription.id_etudiant = id_etudiant
    inscription.id_cours = id_cours
    inscription.id_annee = id_annee

    db.session.commit()

    return {
        "status": "success",
        "message": "Inscription modifiée avec succès.",
        "data": inscription.to_dict()
    }, 200