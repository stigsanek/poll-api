from fastapi import APIRouter

from poll_api.api.api_v1.endpoints import choice, login, question, users

api_router = APIRouter()

api_router.include_router(
    router=login.router,
    tags=['Login']
)
api_router.include_router(
    router=question.router,
    prefix='/questions',
    tags=['Questions']
)
api_router.include_router(
    router=choice.router,
    prefix='/choices',
    tags=['Choices']
)
api_router.include_router(
    router=users.router,
    prefix='/users',
    tags=['Users']
)
