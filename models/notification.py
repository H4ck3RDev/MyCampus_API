from datetime import datetime

from database import db


class Notification(db.Model):

    __tablename__ = "notifications"

    id_notification = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    titre = db.Column(
        db.String(150),
        nullable=False
    )

    contenu = db.Column(
        db.Text,
        nullable=False
    )

    id_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey(
            "utilisateurs.id_utilisateur"
        ),
        nullable=False
    )

    lu = db.Column(
        db.Boolean,
        default=False
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    utilisateur = db.relationship(
        "Utilisateur",
        backref="notifications"
    )

    def to_dict(self):

        return {
            "id_notification": self.id_notification,
            "titre": self.titre,
            "contenu": self.contenu,
            "id_utilisateur": self.id_utilisateur,
            "utilisateur": self.utilisateur.email if self.utilisateur else None,
            "lu": self.lu,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }
