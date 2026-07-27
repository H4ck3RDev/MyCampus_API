from datetime import datetime

from database import db


class Document(db.Model):

    __tablename__ = "documents"

    id_document = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nom = db.Column(
        db.String(255),
        nullable=False
    )

    chemin = db.Column(
        db.String(255),
        nullable=False
    )

    type_document = db.Column(
        db.String(100),
        nullable=True
    )

    id_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey(
            "utilisateurs.id_utilisateur"
        ),
        nullable=True
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    utilisateur = db.relationship(
        "Utilisateur",
        backref="documents"
    )

    def to_dict(self):

        return {
            "id_document": self.id_document,
            "nom": self.nom,
            "chemin": self.chemin,
            "type_document": self.type_document,
            "id_utilisateur": self.id_utilisateur,
            "utilisateur": self.utilisateur.email if self.utilisateur else None,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }
