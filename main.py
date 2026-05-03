from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.projects.router import projects_router
from src.core.exceptions import ProjectServiceException


app = FastAPI()


app.include_router(projects_router)


@app.exception_handler(ProjectServiceException)
async def project_service_exception(request, exc: ProjectServiceException):
    return JSONResponse(status_code=exc.error_code, content={'detail': exc.message})
    
