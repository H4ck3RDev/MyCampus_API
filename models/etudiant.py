from database import db


class Etudiant(db.Model):

    __tablename__ = "etudiants"

    id_etudiant = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    matricule = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    id_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey(
            "utilisateurs.id_utilisateur"
        ),
        nullable=False,
        unique=True
    )

    id_promotion = db.Column(
        db.Integer,
        db.ForeignKey(
            "promotions.id_promotion"
        ),
        nullable=False
    )

    utilisateur = db.relationship(
        "Utilisateur",
        back_populates="etudiant"
    )

    promotion = db.relationship(
        "Promotion",
        back_populates="etudiants"
    )

    inscriptions = db.relationship(
        "Inscription",
        back_populates="etudiant",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_etudiant": self.id_etudiant,

            "matricule": self.matricule,

            "id_utilisateur": self.id_utilisateur,

            "nom": self.utilisateur.nom if self.utilisateur else None,

            "postnom": self.utilisateur.postnom if self.utilisateur else None,

            "prenom": self.utilisateur.prenom if self.utilisateur else None,

            "email": self.utilisateur.email if self.utilisateur else None,

            "id_promotion": self.id_promotion,

            "promotion": self.promotion.nom if self.promotion else None

        }