from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Return password hash

    Args:
        password (str): Password

    Returns:
        str: Password hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifiy password

    Args:
        plain_password (str): Plain password
        hashed_password (str): Password hash

    Returns:
        bool: _description_
    """
    return pwd_context.verify(plain_password, hashed_password)
