from database import db


class Cours(db.Model):

    __tablename__ = "cours"

    id_cours = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    code_cours = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    nom_cours = db.Column(
        db.String(100),
        nullable=False
    )

    credit = db.Column(
        db.Integer,
        default=0
    )

    volume_horaire = db.Column(
        db.Integer,
        default=0
    )

    id_departement = db.Column(
        db.Integer,
        db.ForeignKey(
            "departements.id_departement"
        ),
        nullable=False
    )

    departement = db.relationship(
        "Departement",
        back_populates="cours"
    )

    affectations = db.relationship(
        "AffectationProfesseur",
        back_populates="cours",
        cascade="all, delete-orphan"
    )

    inscriptions = db.relationship(
        "Inscription",
        back_populates="cours",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_cours": self.id_cours,

            "code_cours": self.code_cours,

            "nom_cours": self.nom_cours,

            "credit": self.credit,

            "volume_horaire": self.volume_horaire,

            "id_departement": self.id_departement,

            "departement": self.departement.nom
            if self.departement else None
        }