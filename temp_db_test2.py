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
    res = conn.execute(text('SELECT id_departement, nom FROM departements LIMIT 5'))
    print('DEPARTEMENTS:')
    for row in res:
        print(row)
