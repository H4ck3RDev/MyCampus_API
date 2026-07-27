from database import db
from datetime import datetime


class Utilisateur(db.Model):

    __tablename__ = "utilisateurs"


    id_utilisateur = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )


    nom = db.Column(
        db.String(50),
        nullable=False
    )


    postnom = db.Column(
        db.String(50)
    )


    prenom = db.Column(
        db.String(50)
    )


    sexe = db.Column(
        db.Enum("M", "F"),
        nullable=True
    )


    date_naissance = db.Column(
        db.Date,
        nullable=True
    )


    telephone = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )


    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    mot_de_passe = db.Column(
        db.String(255),
        nullable=False
    )


    photo = db.Column(
        db.String(255),
        nullable=True
    )


    statut = db.Column(
        db.Enum(
            "actif",
            "inactif",
            "suspendu"
        ),
        default="actif"
    )


    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    id_role = db.Column(
        db.Integer,
        db.ForeignKey(
            "roles.id_role"
        ),
        nullable=False
    )


    # Relation Role
    role = db.relationship(
        "Role",
        back_populates="utilisateurs"
    )

    etudiant = db.relationship(
        "Etudiant",
        back_populates="utilisateur",
        uselist=False,
        cascade="all, delete-orphan"
    )

    professeur = db.relationship(
        "Professeur",
        back_populates="utilisateur",
        uselist=False,
        cascade="all, delete"
    )


    def to_dict(self):

        return {

            "id_utilisateur":
                self.id_utilisateur,

            "nom":
                self.nom,

            "postnom":
                self.postnom,

            "prenom":
                self.prenom,

            "sexe":
                self.sexe,

            "date_naissance":
                str(self.date_naissance)
                if self.date_naissance else None,

            "telephone":
                self.telephone,

            "email":
                self.email,

            "photo":
                self.photo,

            "statut":
                self.statut,

            "date_creation":
                self.date_creation.isoformat()
                if self.date_creation else None,

            "id_role":
                self.id_role,

            "role":
                self.role.nom_role
                if self.role else None

        }