import os
from pathlib import Path
from sqlalchemy import create_engine, text

env_path = Path(r'C:\Users\PC\MesProjets\mycampus_api\.env')
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())
uri = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
engine = create_engine(uri)
with engine.connect() as conn:
    for query,label in [
        ("SELECT id_etudiant, matricule FROM etudiants LIMIT 10", 'etudiants'),
        ("SELECT id_cours, code_cours, nom_cours FROM cours LIMIT 10", 'cours'),
        ("SELECT id_annee, libelle FROM annees_academiques LIMIT 10", 'annees')
    ]:
        print('--', label)
        for row in conn.execute(text(query)):
            print(row)
