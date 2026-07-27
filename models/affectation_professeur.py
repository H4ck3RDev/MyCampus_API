from database import db


class AffectationProfesseur(db.Model):

    __tablename__ = "affectations_professeurs"

    id_affectation = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_professeur = db.Column(
        db.Integer,
        db.ForeignKey("professeurs.id_professeur"),
        nullable=False
    )

    id_cours = db.Column(
        db.Integer,
        db.ForeignKey("cours.id_cours"),
        nullable=False
    )

    id_annee = db.Column(
        db.Integer,
        db.ForeignKey("annees_academiques.id_annee"),
        nullable=False
    )

    professeur = db.relationship(
        "Professeur",
        back_populates="affectations"
    )

    cours = db.relationship(
        "Cours",
        back_populates="affectations"
    )

    annee = db.relationship(
        "AnneeAcademique"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_professeur",
            "id_cours",
            name="uq_professeur_cours"
        ),
    )

    def to_dict(self):

        return {

            "id_affectation": self.id_affectation,

            "id_professeur": self.id_professeur,

            "id_cours": self.id_cours,

            "id_annee": self.id_annee,

            "professeur": {
                "id_professeur": self.professeur.id_professeur,
                "nom": self.professeur.utilisateur.nom if self.professeur and self.professeur.utilisateur else None,
                "postnom": self.professeur.utilisateur.postnom if self.professeur and self.professeur.utilisateur else None,
                "prenom": self.professeur.utilisateur.prenom if self.professeur and self.professeur.utilisateur else None,
                "email": self.professeur.utilisateur.email if self.professeur and self.professeur.utilisateur else None,
                "grade": self.professeur.grade,
                "specialite": self.professeur.specialite
            } if self.professeur else None,

            "cours": {
                "id_cours": self.cours.id_cours,
                "code_cours": self.cours.code_cours,
                "nom_cours": self.cours.nom_cours,
                "credit": self.cours.credit,
                "volume_horaire": self.cours.volume_horaire
            } if self.cours else None,

            "annee": {
                "id_annee": self.annee.id_annee,
                "libelle": self.annee.libelle,
                "date_debut": self.annee.date_debut.isoformat() if self.annee and self.annee.date_debut else None,
                "date_fin": self.annee.date_fin.isoformat() if self.annee and self.annee.date_fin else None
            } if self.annee else None

        }