from loguru import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.board import projects_router, webhook_router
from src.auth import auth_router
from src.core.exceptions import ProjectServiceException
from src.core.middleware import logging_middleware
from src.ai.routes import ai_router

logger.info('Start app')
app = FastAPI()

app.include_router(projects_router, prefix='/projects', tags=['projects'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(webhook_router)

app.include_router(ai_router)

app.middleware("http")(logging_middleware)

@app.get('/index')
async def index():
    return {'Me': 'KING'}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ProjectServiceException)  # TODO: project global base exception
async def project_service_exception(request, exc: ProjectServiceException):
    logger.warning(f'Custom Exception {exc.message}')
    return JSONResponse(status_code=exc.error_code, content={"detail": exc.message})
