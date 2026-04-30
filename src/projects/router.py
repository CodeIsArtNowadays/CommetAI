from fastapi.routing import APIRouter

from src.projects.schemas import ProjectRetrieveSchema


projects_router = APIRouter()


@projects_router.get('/', response_model=ProjectRetrieveSchema)
async def get_projects():
    pass