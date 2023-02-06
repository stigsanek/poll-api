import json

from tests import FIXTURES_DIR


def read_json_fixture(file: str) -> dict:
    """Return json-fixture data

    Args:
        file (str): File name

    Returns:
        dict: Data
    """
    with open(file=FIXTURES_DIR / file) as f:
        return json.loads(f.read())
