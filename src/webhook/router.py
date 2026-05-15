from fastapi import APIRouter, Request, Depends

from src.webhook.dependencies import get_wh_service
from src.webhook.service import WebhookService
from src.webhook.schemas import WhRecordCreateSchema


wh_router = APIRouter()


@wh_router.post('/webhook/event')
async def webhook_callback(
    request: Request,
    wh_service: WebhookService = Depends(get_wh_service)
):
    signatre = request.headers.get('x-hub-signature')  # TODO: verif with github_secret 
    delivery = request.headers.get('x-github-delivery')  # TODO: save to redis, avoid double handling
    
    response_data = await request.json()
    
    if request.headers.get('x-github-event') == 'ping':
        # TODO: wh created
        # await wh_service.repo.create_webhook_record()
        # return 200
        pass
        
    
    
    
    print(request.headers)
    
    return {'wh': 'on'}
    
    
    
    
{
'zen': 'Avoid administrative distraction.', 
'hook_id': 624276416, 
'hook': 
    {
        'type': 'Repository', 
        'id': 624276416, 
        'name': 'web', 
        'active': True, 
        'events': ['push'], 
        'config': {'content_type': 'json', 'insecure_ssl': '0', 'secret': '********', 'url': 'https://peddling-unsure-unpaid.ngrok-free.dev/webhooks/github'}, 
        'updated_at': '2026-05-15T18:48:04Z', 
        'created_at': '2026-05-15T18:48:04Z', 
        'url': 'https://api.github.com/repos/CodeIsArtNowadays/test1/hooks/624276416', 
        'test_url': 'https://api.github.com/repos/CodeIsArtNowadays/test1/hooks/624276416/test', 
        'ping_url': 'https://api.github.com/repos/CodeIsArtNowadays/test1/hooks/624276416/pings', 
        'deliveries_url': 'https://api.github.com/repos/CodeIsArtNowadays/test1/hooks/624276416/deliveries', 
        'last_response': {'code': None, 'status': 'unused', 'message': None}
    }, 
    'repository': 
        {
            'id': 1239046408, 
            'node_id': 'R_kgDOSdpZCA', 
            'name': 'test1', 
            'full_name': 'CodeIsArtNowadays/test1', 
            'private': False, 
            'owner': {'login': 'CodeIsArtNowadays', 'id': 93353343, 'node_id': 'U_kgDOBZB1fw', 'avatar_url': 'https://avatars.githubusercontent.com/u/93353343?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/CodeIsArtNowadays', 'html_url': 'https://github.com/CodeIsArtNowadays', 'followers_url': 'https://api.github.com/users/CodeIsArtNowadays/followers', 'following_url': 'https://api.github.com/users/CodeIsArtNowadays/following{/other_user}', 'gists_url': 'https://api.github.com/users/CodeIsArtNowadays/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/CodeIsArtNowadays/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/CodeIsArtNowadays/subscriptions', 'organizations_url': 'https://api.github.com/users/CodeIsArtNowadays/orgs', 'repos_url': 'https://api.github.com/users/CodeIsArtNowadays/repos', 'events_url': 'https://api.github.com/users/CodeIsArtNowadays/events{/privacy}', 'received_events_url': 'https://api.github.com/users/CodeIsArtNowadays/received_events', 'type': 'User', 'user_view_type': 'public', 'site_admin': False}, 'html_url': 'https://github.com/CodeIsArtNowadays/test1', 'description': None, 'fork': False, 'url': 'https://api.github.com/repos/CodeIsArtNowadays/test1', 'forks_url': 'https://api.