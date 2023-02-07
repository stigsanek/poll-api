import os
from collections import namedtuple
from pathlib import Path

from poll_api.config import settings

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

FAKE_PASSWORD = 'fake_password'

FAKE_DB = 'fakedb.sqlite3'

APIUrls = namedtuple('APIUrls', ('login', 'users', 'questions'))
urls = APIUrls(
    login=f'{settings.API_V1}/login',
    users=f'{settings.API_V1}/users',
    questions=f'{settings.API_V1}/questions',
)

try:
    os.remove(FAKE_DB)
except FileNotFoundError:
    pass

settings.DATABASE_URL = f'sqlite:///{FAKE_DB}'
