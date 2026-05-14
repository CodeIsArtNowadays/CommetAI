from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.board import projects_router
from src.auth import auth_router
from src.core.exceptions import ProjectServiceException

app = FastAPI()


app.include_router(projects_router, prefix='/projects', tags=['projects'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])

@app.get('/index')
async def index():
    return {'Me': 'KING'}
    
@app.post('/webhooks/github')
async def wh(data):
    print('check2')
    print(data)

@app.exception_handler(ProjectServiceException)  # TODO: project global base exception
async def project_service_exception(request, exc: ProjectServiceException):
    return JSONResponse(status_code=exc.error_code, content={"detail": exc.message})


@app.on_event("startup")
async def startup():
    from src.core.database import Base, engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
