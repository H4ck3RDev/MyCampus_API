from datetime import datetime

from database import db


class Note(db.Model):

    __tablename__ = "notes"

    id_note = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    valeur = db.Column(
        db.Float,
        nullable=False
    )

    type_note = db.Column(
        db.String(50),
        nullable=True
    )

    commentaire = db.Column(
        db.String(255),
        nullable=True
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
        nullable=False
    )

    id_professeur = db.Column(
        db.Integer,
        db.ForeignKey(
            "professeurs.id_professeur"
        ),
        nullable=True
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    etudiant = db.relationship(
        "Etudiant",
        backref="notes"
    )

    cours = db.relationship(
        "Cours",
        backref="notes"
    )

    professeur = db.relationship(
        "Professeur",
        backref="notes"
    )

    def to_dict(self):

        return {
            "id_note": self.id_note,
            "valeur": self.valeur,
            "type_note": self.type_note,
            "commentaire": self.commentaire,
            "id_etudiant": self.id_etudiant,
            "nom_etudiant": self.etudiant.utilisateur.nom if self.etudiant and self.etudiant.utilisateur else None,
            "prenom_etudiant": self.etudiant.utilisateur.prenom if self.etudiant and self.etudiant.utilisateur else None,
            "id_cours": self.id_cours,
            "cours": self.cours.nom_cours if self.cours else None,
            "id_professeur": self.id_professeur,
            "professeur": self.professeur.utilisateur.nom if self.professeur and self.professeur.utilisateur else None,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }
