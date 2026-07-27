from database import db


class Departement(db.Model):

    __tablename__ = "departements"

    id_departement = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    id_faculte = db.Column(
        db.Integer,
        db.ForeignKey("facultes.id_faculte"),
        nullable=False
    )

    # Relation avec Faculté
    faculte = db.relationship(
        "Faculte",
        back_populates="departements"
    )

    promotions = db.relationship(
        "Promotion",
        back_populates="departement",
        cascade="all, delete-orphan"
    )

    cours = db.relationship(
        "Cours",
        back_populates="departement",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_departement": self.id_departement,

            "nom": self.nom,

            "description": self.description,

            "id_faculte": self.id_faculte,

            "faculte": self.faculte.nom
            if self.faculte else None

        }