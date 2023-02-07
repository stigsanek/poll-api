from collections import namedtuple
from pathlib import Path

from poll_api.config import settings

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

FAKE_PASSWORD = 'fake_password'

APIUrls = namedtuple('APIUrls', ('login', 'users', 'questions'))
urls = APIUrls(
    login=f'{settings.API_V1}/login',
    users=f'{settings.API_V1}/users',
    questions=f'{settings.API_V1}/questions',
)

settings.DATABASE_URL = 'sqlite:///db.sqlite3'
