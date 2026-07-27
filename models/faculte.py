from database import db


class Faculte(db.Model):

    __tablename__ = "facultes"

    id_faculte = db.Column(
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

    departements = db.relationship(
        "Departement",
        back_populates="faculte",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_faculte": self.id_faculte,

            "nom": self.nom,

            "description": self.description

        }