from fastapi import Depends
from fastapi.routing import APIRouter

from src.projects.schemas import ProjectRetrieveSchema, ProjectCreateRequestSchema, ProjectUpdateSchema
from src.projects.service import ProjectService
from src.auth.models import User
from src.core.dependencies import get_mock_user, get_project_service


projects_router = APIRouter()


@projects_router.get('/', response_model=list[ProjectRetrieveSchema])
async def get_all_projects(
    user: User = Depends(get_mock_user),
    service: ProjectService = Depends(get_project_service)
):
    pass


@projects_router.get('/{project_id}', response_model=ProjectRetrieveSchema)
async def get_project_by_id(
    project_id: int,
    user: User = Depends(get_mock_user),
    service: ProjectService = Depends(get_project_service)
):
    pass

@projects_router.post(
    '/',
    response_model=ProjectRetrieveSchema,
    status_code=201
)
async def create_project(
    project_data: ProjectCreateRequestSchema,
    user: User = Depends(get_mock_user),
    service: ProjectService = Depends(get_project_service)
):
    pass

@projects_router.patch('/{project_id}', response_model=ProjectRetrieveSchema)
async def update_project(
    project_id: int, 
    updated_project: ProjectUpdateSchema,
    user: User = Depends(get_mock_user),
    service: ProjectService = Depends(get_project_service)
):
    pass

@projects_router.delete('/{project_id}', status_code=204)
async def delete_project(
    project_id: int,
    user: User = Depends(get_mock_user),
    service: ProjectService = Depends(get_project_service)
):
    pass
