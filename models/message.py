from datetime import datetime

from database import db


class Message(db.Model):

    __tablename__ = "messages"

    id_message = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    sujet = db.Column(
        'objet',
        db.String(100),
        nullable=False
    )

    contenu = db.Column(
        db.Text,
        nullable=False
    )

    id_expediteur = db.Column(
        db.Integer,
        db.ForeignKey(
            "utilisateurs.id_utilisateur"
        ),
        nullable=False
    )

    id_destinataire = db.Column(
        db.Integer,
        db.ForeignKey(
            "utilisateurs.id_utilisateur"
        ),
        nullable=False
    )

    date_envoi = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    lu = db.Column(
        db.Boolean,
        default=False
    )

    expediteur = db.relationship(
        "Utilisateur",
        foreign_keys=[id_expediteur],
        backref="messages_envoyes"
    )

    destinataire = db.relationship(
        "Utilisateur",
        foreign_keys=[id_destinataire],
        backref="messages_recus"
    )

    def to_dict(self):

        return {
            "id_message": self.id_message,
            "sujet": self.sujet,
            "contenu": self.contenu,
            "id_expediteur": self.id_expediteur,
            "expediteur": self.expediteur.email if self.expediteur else None,
            "id_destinataire": self.id_destinataire,
            "destinataire": self.destinataire.email if self.destinataire else None,
            "date_envoi": self.date_envoi.isoformat() if self.date_envoi else None,
            "lu": bool(self.lu)
        }
