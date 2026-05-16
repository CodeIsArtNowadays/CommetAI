import hashlib
import hmac
import json

import httpx
from fastapi import Depends, Request
from fastapi.routing import APIRouter

from config import settings
from src.board.schemas import ProjectRetrieveSchema, ProjectCreateRequestSchema, ProjectUpdateSchema
from src.board.service import ProjectService
from src.auth.models import User
from src.core.dependencies import get_user
from src.board.dependencies import get_project_service


projects_router = APIRouter()
webhook_router = APIRouter()


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
    return await service.get_project_by_id(project_id, user.id)

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
    project_service: ProjectService = Depends(get_project_service)
):
    body = await request.body()
    response_data = json.loads(body)
    
    event = request.headers.get('x-github-event')
    delivery = request.headers.get('x-github-delivery')  # TODO: save to redis, avoid double handling
    
    if event == 'ping':
        print('ping')
        return 200
        
    if event == 'push':
        
        repo_full_name = response_data['repository']['full_name']

        project = await project_service.repo.get_project_by_repo_full_name(repo_full_name)
        
        signature = request.headers.get('x-hub-signature-256')
        
        if not signature:
            raise Exception  # TODO: exc
        
        secret = project.webhook_secret
        
        expected = 'sha256=' + hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected, signature):
            return 400 # TODO: exc
            
        
        # Commits handling
        # 
        
        for commit in response_data['commits']:
            commit_id = commit['id']
            
            async with httpx.AsyncClient() as client:
                url = f'https://api.github.com/repos/{repo_full_name}/commits/{commit_id}'
                headers = {
                    'Authorization': f'Bearer {project.owner.github_token}',
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
                response = await client.get(
                    url,
                    headers=headers
                )

                response_data = response.json()
                
                commit_data = {
                    'sha': response_data['sha'],
                    'commit_message': response_data.get('commit').get('message'),
                    'commit_author_name': response_data.get('commit').get('author').get('name'),
                    'commit_created': response_data.get('commit').get('author').get('date'),
                    'additions': response_data.get('stats').get('additions'),
                    'deletions': response_data.get('stats').get('deletions'),
                    'files': response_data.get('files')
                }
                
                print(commit_data)
    
    return 
