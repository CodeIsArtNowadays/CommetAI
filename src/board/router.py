import json

from fastapi import Depends, Request, Response, BackgroundTasks
from fastapi.routing import APIRouter
from redis.asyncio import Redis

from src.board.process_push import ProcessPushUseCase
from src.core.exceptions import WebhookNotVerify
from src.board.schemas import ProjectRetrieveSchema, ProjectCreateRequestSchema, ProjectUpdateSchema, TasksAllRetreiveSchema
from src.board.project_service import ProjectService, WebhookService
from src.auth.models import User
from src.core.dependencies import get_redis_cli, get_user
from src.board.dependencies import get_project_service, get_webhook_service


projects_router = APIRouter()
webhook_router = APIRouter()
tasks_router = APIRouter(prefix='/projects/{project_id}')




@projects_router.get('/', response_model=list[ProjectRetrieveSchema])
async def get_all_projects(
    user: User = Depends(get_user),
    service: ProjectService = Depends(get_project_service),
):
    return await service.get_all_project_by_user(user.id)

@projects_router.get('/{project_id}', response_model=ProjectRetrieveSchema)
async def get_project_by_id(
    project_id: int,
    user: User = Depends(get_user),
    service: ProjectService = Depends(get_project_service)
):
    return await service.repo.get_project_with_tasks_and_commits(project_id)

@tasks_router.get('/tasks', response_model=TasksAllRetreiveSchema)
async def get_all_tasks_by_project(project_id: int, user: User = Depends(get_user),
service: ProjectService = Depends(get_project_service)):
    return await service.repo.get_all_tasks_by_project_id(project_id)


@projects_router.patch('/{project_id}', response_model=ProjectRetrieveSchema)
async def update_project(
    project_id: int, 
    updated_project: ProjectUpdateSchema,
    user: User = Depends(get_user),
    service: ProjectService = Depends(get_project_service)
):
    return await service.update_project(project_id, updated_project, user.id)

@projects_router.delete('/{project_id}', status_code=204)
async def delete_project(
    project_id: int,
    user: User = Depends(get_user),
    service: ProjectService = Depends(get_project_service)
):
    await service.delete_project(project_id, user.id)

@projects_router.post(
    '/',
    response_model=ProjectRetrieveSchema,
    status_code=201
)
async def create_project(
    project_data: ProjectCreateRequestSchema,
    user: User = Depends(get_user),
    service: ProjectService = Depends(get_project_service)
):
    return await service.create_project(project_data, user)


@webhook_router.post('/webhook/event')
async def webhook_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    project_service: ProjectService = Depends(get_project_service),
    webhook_service: WebhookService = Depends(get_webhook_service),
    use_case: ProcessPushUseCase = Depends(ProcessPushUseCase),
    redis: Redis = Depends(get_redis_cli)
):
    body = await request.body()
    event = request.headers.get('x-github-event')
    if event == 'ping':
        return Response(status_code=200)
    
    
    delivery = request.headers.get('x-github-delivery')
    
    delivery_check_error = (not bool(delivery)) or bool(await redis.get(delivery))
    
    if delivery_check_error:
        raise WebhookNotVerify
    else:
        await redis.set(delivery, True, ex=604800)  # type: ignore

    if event == 'push':
        response_data = json.loads(body)
        repo_full_name = response_data['repository']['full_name']

        project = await project_service.repo.get_project_by_repo_full_name(repo_full_name)
        
        signature = request.headers.get('x-hub-signature-256')
        
        if not signature:
            raise WebhookNotVerify  
        
        if not await webhook_service.verify_webhook_request(signature, project.webhook_secret, body):
            raise WebhookNotVerify  
        
        push_data = {
            'project_id': project.id,
            'project_description': project.description,
            'commits': response_data['commits'],
            'repo_full_name': repo_full_name,
            'owner_github_token': project.owner.github_token
        }
        background_tasks.add_task(use_case, push_data)
    
    return Response(status_code=200)

