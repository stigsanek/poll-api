import os
from pathlib import Path

from poll_api.config import settings

FIXTURES_DIR = Path(__file__).parent / 'fixtures'
FAKE_PASSWORD = 'Test!123'
FAKE_DB = 'fakedb.sqlite3'

try:
    os.remove(FAKE_DB)
except FileNotFoundError:
    pass

settings.DATABASE_URL = f'sqlite:///{FAKE_DB}'
