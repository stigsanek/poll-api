from collections import namedtuple
from pathlib import Path

from poll_api.config import settings

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

FAKE_PASSWORD = 'fake_password'

APIUrls = namedtuple(
    typename='APIUrls',
    field_names=('login', 'choices', 'questions', 'users')
)
urls = APIUrls(
    login=f'{settings.API_V1}/login',
    choices=f'{settings.API_V1}/choices',
    questions=f'{settings.API_V1}/questions',
    users=f'{settings.API_V1}/users'
)

settings.DATABASE_URL = 'sqlite:///db.sqlite3'
