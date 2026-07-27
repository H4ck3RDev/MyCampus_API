from datetime import datetime

from database import db


class Presence(db.Model):

    __tablename__ = "presences"

    id_presence = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_etudiant = db.Column(
        db.Integer,
        db.ForeignKey(
            "etudiants.id_etudiant"
        ),
        nullable=False
    )

    id_cours = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours.id_cours"
        ),
        nullable=True
    )

    date_presence = db.Column(
        db.Date,
        nullable=False
    )

    statut = db.Column(
        db.Enum("Présent", "Absent", "Retard"),
        default="Présent"
    )

    etudiant = db.relationship(
        "Etudiant",
        backref="presences"
    )

    cours = db.relationship(
        "Cours",
        backref="presences"
    )

    def to_dict(self):

        return {
            "id_presence": self.id_presence,
            "id_etudiant": self.id_etudiant,
            "nom_etudiant": self.etudiant.utilisateur.nom if self.etudiant and self.etudiant.utilisateur else None,
            "id_cours": self.id_cours,
            "cours": self.cours.nom_cours if self.cours else None,
            "date_presence": self.date_presence.isoformat() if self.date_presence else None,
            "statut": self.statut
        }
