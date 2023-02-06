import os
from collections import namedtuple
from pathlib import Path

from poll_api.config import settings

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

FAKE_PASSWORD = 'fake_password'

FAKE_DB = 'fakedb.sqlite3'

APIUrls = namedtuple('APIUrls', ('users', 'login'))
urls = APIUrls(
    users=f'{settings.API_V1}/users',
    login=f'{settings.API_V1}/login'
)

try:
    os.remove(FAKE_DB)
except FileNotFoundError:
    pass

settings.DATABASE_URL = f'sqlite:///{FAKE_DB}'
