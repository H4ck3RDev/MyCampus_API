from database import db


class Promotion(db.Model):

    __tablename__ = "promotions"

    id_promotion = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    niveau = db.Column(
        db.String(20)
    )

    id_departement = db.Column(
        db.Integer,
        db.ForeignKey("departements.id_departement"),
        nullable=False
    )

    departement = db.relationship(
        "Departement",
        back_populates="promotions"
    )

    etudiants = db.relationship(
        "Etudiant",
        back_populates="promotion",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_promotion": self.id_promotion,

            "nom": self.nom,

            "niveau": self.niveau,

            "id_departement": self.id_departement,

            "departement": self.departement.nom
            if self.departement else None

        }