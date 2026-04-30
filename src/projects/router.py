from fastapi.routing import APIRouter

from src.projects.schemas import ProjectRetrieveSchema, ProjectRequestByID


projects_router = APIRouter()


@projects_router.get('/', response_model=list[ProjectRetrieveSchema])
async def get_all_projects():
    pass


@projects_router.get('/{project_id}', response_model=ProjectRetrieveSchema)
async def get_project_by_id(id: ProjectRequestByID, ):
    pass