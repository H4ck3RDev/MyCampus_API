from database import db


class Professeur(db.Model):

    __tablename__ = "professeurs"

    id_professeur = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    grade = db.Column(
        db.String(50)
    )

    specialite = db.Column(
        db.String(100)
    )

    id_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey("utilisateurs.id_utilisateur"),
        unique=True,
        nullable=False
    )

    utilisateur = db.relationship(
        "Utilisateur",
        back_populates="professeur"
    )

    affectations = db.relationship(
        "AffectationProfesseur",
        back_populates="professeur",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {

            "id_professeur": self.id_professeur,

            "nom": self.utilisateur.nom if self.utilisateur else None,

            "postnom": self.utilisateur.postnom if self.utilisateur else None,

            "prenom": self.utilisateur.prenom if self.utilisateur else None,

            "email": self.utilisateur.email if self.utilisateur else None,

            "telephone": self.utilisateur.telephone if self.utilisateur else None,

            "grade": self.grade,

            "specialite": self.specialite

        }