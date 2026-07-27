from database import db


class Inscription(db.Model):

    __tablename__ = "inscriptions"

    id_inscription = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_etudiant = db.Column(
        db.Integer,
        db.ForeignKey("etudiants.id_etudiant"),
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

    date_inscription = db.Column(
        db.Date,
        server_default=db.text("curdate()")
    )

    etudiant = db.relationship(
        "Etudiant",
        back_populates="inscriptions"
    )

    cours = db.relationship(
        "Cours",
        back_populates="inscriptions"
    )

    annee = db.relationship(
        "AnneeAcademique",
        back_populates="inscriptions"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_etudiant",
            "id_cours",
            "id_annee",
            name="uq_inscription_etudiant_cours_annee"
        ),
    )

    def to_dict(self):
        return {
            "id_inscription": self.id_inscription,
            "id_etudiant": self.id_etudiant,
            "id_cours": self.id_cours,
            "id_annee": self.id_annee,
            "date_inscription": self.date_inscription.isoformat() if self.date_inscription else None,
            "etudiant": {
                "id_etudiant": self.etudiant.id_etudiant,
                "nom": self.etudiant.utilisateur.nom if self.etudiant and self.etudiant.utilisateur else None,
                "postnom": self.etudiant.utilisateur.postnom if self.etudiant and self.etudiant.utilisateur else None,
                "prenom": self.etudiant.utilisateur.prenom if self.etudiant and self.etudiant.utilisateur else None,
                "email": self.etudiant.utilisateur.email if self.etudiant and self.etudiant.utilisateur else None
            } if self.etudiant else None,
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