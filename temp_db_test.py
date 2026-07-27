import os
from pathlib import Path
env_path = Path(r'C:\Users\PC\MesProjets\mycampus_api\.env')
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())
from sqlalchemy import create_engine, text
uri = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
print('URI', uri)
engine = create_engine(uri)
with engine.connect() as conn:
    for tbl in ['professeurs','cours','annees_academiques']:
        try:
            print('TABLE', tbl)
            res = conn.execute(text(f"SELECT * FROM {tbl} LIMIT 5"))
            for row in res:
                print(row)
        except Exception as e:
            print('ERR', tbl, e)
