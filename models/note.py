from database import db


class Note(db.Model):

    __tablename__ = "notes"

    id_note = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_etudiant = db.Column(
        db.Integer,
        db.ForeignKey(
            "etudiants.id_etudiant"
        ),
        nullable=False
    )

    id_cours = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours.id_cours"
        ),
        nullable=False
    )

    tp = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    interrogation = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    examen = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    moyenne = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    etudiant = db.relationship(
        "Etudiant",
        backref="notes"
    )

    cours = db.relationship(
        "Cours",
        backref="notes"
    )

    def to_dict(self):
        return {
            "id_note": self.id_note,
            "id_etudiant": self.id_etudiant,
            "nom_etudiant": self.etudiant.utilisateur.nom if self.etudiant and self.etudiant.utilisateur else None,
            "prenom_etudiant": self.etudiant.utilisateur.prenom if self.etudiant and self.etudiant.utilisateur else None,
            "id_cours": self.id_cours,
            "cours": self.cours.nom_cours if self.cours else None,
            "tp": float(self.tp) if self.tp is not None else None,
            "interrogation": float(self.interrogation) if self.interrogation is not None else None,
            "examen": float(self.examen) if self.examen is not None else None,
            "moyenne": float(self.moyenne) if self.moyenne is not None else None
        }
