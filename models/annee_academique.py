from database import db

class AnneeAcademique(db.Model):

    __tablename__ = "annees_academiques"

    id_annee = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    libelle = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    date_debut = db.Column(
        db.Date
    )

    date_fin = db.Column(
        db.Date
    )

    inscriptions = db.relationship(
        "Inscription",
        back_populates="annee",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_annee": self.id_annee,

            "libelle": self.libelle,

            "date_debut":
                self.date_debut.isoformat()
                if self.date_debut else None,

            "date_fin":
                self.date_fin.isoformat()
                if self.date_fin else None
        }