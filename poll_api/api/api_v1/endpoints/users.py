from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def index() -> dict:
    return {'msg': 'Hello, World!'}
