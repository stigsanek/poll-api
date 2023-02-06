from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from poll_api.api.api_v1.api import api_router
from poll_api.config import settings
from poll_api.db import engine
from poll_api.models import Base

Base.metadata.create_all(engine)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1}/openapi.json'
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(url) for url in settings.BACKEND_CORS_ORIGINS],
        allow_methods=['*'],
        allow_headers=['*']
    )

app.include_router(api_router, prefix=settings.API_V1)
