from models.role import Role
from models.utilisateur import Utilisateur
from models.annee_academique import AnneeAcademique
from models.faculte import Faculte
from models.departement import Departement
from models.promotion import Promotion
from models.etudiant import Etudiant
from models.professeur import Professeur
from models.affectation_professeur import AffectationProfesseur
from models.inscription import Inscription
from .cours import Cours


__all__ = [

    "Role",

    "Utilisateur",

    "AnneeAcademique",

    "Faculte",

    "Departement",

    "Promotion",

    "Etudiant",

    "Professeur",
    
    "AffectationProfesseur",
    
    "Inscription",
    
    "Cours"
]