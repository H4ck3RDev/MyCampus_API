from database import db


class Role(db.Model):

    __tablename__ = "roles"


    id_role = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )


    nom_role = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=True
    )


    # Relation avec Utilisateur
    utilisateurs = db.relationship(
        "Utilisateur",
        back_populates="role",
        lazy=True
    )


    def to_dict(self):

        return {

            "id_role": self.id_role,

            "nom_role": self.nom_role,

            "description": self.description

        }