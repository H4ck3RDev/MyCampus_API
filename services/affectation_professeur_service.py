from database import db

from models.affectation_professeur import AffectationProfesseur
from models.professeur import Professeur
from models.cours import Cours
from models.annee_academique import AnneeAcademique


def creer_affectation_professeur(data):

    id_professeur = data.get("id_professeur")
    id_cours = data.get("id_cours")
    id_annee = data.get("id_annee")

    if id_professeur is None or id_cours is None or id_annee is None:
        return {
            "status": "error",
            "message": "Les champs id_professeur, id_cours et id_annee sont requis."
        }, 400

    professeur = Professeur.query.get(id_professeur)
    if professeur is None:
        return {
            "status": "error",
            "message": "Professeur introuvable."
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

    existing = AffectationProfesseur.query.filter_by(
        id_professeur=id_professeur,
        id_cours=id_cours,
        id_annee=id_annee
    ).first()

    if existing is not None:
        return {
            "status": "error",
            "message": "Cette affectation existe déjà."
        }, 400

    affectation = AffectationProfesseur(
        id_professeur=id_professeur,
        id_cours=id_cours,
        id_annee=id_annee
    )

    db.session.add(affectation)
    db.session.commit()

    return {
        "status": "success",
        "message": "Affectation professeur créée avec succès.",
        "data": affectation.to_dict()
    }, 201


def modifier_affectation_professeur(affectation, data):

    id_professeur = data.get("id_professeur", affectation.id_professeur)
    id_cours = data.get("id_cours", affectation.id_cours)
    id_annee = data.get("id_annee", affectation.id_annee)

    professeur = Professeur.query.get(id_professeur)
    if professeur is None:
        return {
            "status": "error",
            "message": "Professeur introuvable."
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

    existing = AffectationProfesseur.query.filter(
        AffectationProfesseur.id_professeur == id_professeur,
        AffectationProfesseur.id_cours == id_cours,
        AffectationProfesseur.id_annee == id_annee,
        AffectationProfesseur.id_affectation != affectation.id_affectation
    ).first()

    if existing is not None:
        return {
            "status": "error",
            "message": "Une affectation identique existe déjà."
        }, 400

    affectation.id_professeur = id_professeur
    affectation.id_cours = id_cours
    affectation.id_annee = id_annee

    db.session.commit()

    return {
        "status": "success",
        "message": "Affectation professeur modifiée avec succès.",
        "data": affectation.to_dict()
    }, 200