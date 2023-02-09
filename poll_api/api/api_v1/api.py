from fastapi import APIRouter

from poll_api.api.api_v1.endpoints import choice, login, question, users, vote

api_router = APIRouter()

api_router.include_router(
    router=login.router,
    tags=['login']
)
api_router.include_router(
    router=question.router,
    prefix='/questions',
    tags=['questions']
)
api_router.include_router(
    router=choice.router,
    prefix='/choices',
    tags=['choices']
)
api_router.include_router(
    router=vote.router,
    prefix='/votes',
    tags=['votes']
)
api_router.include_router(
    router=users.router,
    prefix='/users',
    tags=['users']
)
