from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.exceptions import ProjectServiceException
from src.projects.router import projects_router

app = FastAPI()


app.include_router(projects_router, prefix='/projects')


@app.exception_handler(ProjectServiceException)
async def project_service_exception(request, exc: ProjectServiceException):
    return JSONResponse(status_code=exc.error_code, content={"detail": exc.message})


@app.on_event("startup")
async def startup():
    from src.core.database import Base, engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
