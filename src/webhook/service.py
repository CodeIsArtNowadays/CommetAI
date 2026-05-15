import httpx
import uuid

from src.webhook.repository import WebhookRepository
from src.webhook.schemas import WhRecordCreateSchema


class WebhookService:
    
    def __init__(self, repo: WebhookRepository):
        self.repo = repo
        self.base_url = 'https://api.github.com'
        self.wh_callback_url = 'https://peddling-unsure-unpaid.ngrok-free.dev/webhooks/github'
        
        
    async def create_webhook(self, owner: str, owner_github_token: str, repo):
        # httpx request to github with owner/repo
        # get webhook_id from response 
        # save to db
        
        url = self.base_url + f'/repos/{owner}/{repo.title}/hooks'
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {owner_github_token}",
        }
        secret = str(uuid.uuid4())
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, 
                headers=headers,
                json={
                    'name': 'web',
                    'active': True,
                    'events': ['push'],
                    'config': {
                        'url': self.wh_callback_url,
                        'content_type': 'json',
                        'secret': secret,
                    }
                }
            )
            
            if response.status_code == 200:
            
                response_data = await response.json()
                wh_record_data = WhRecordCreateSchema(
                    repo_id=repo.id,
                    webhook_id=response_data['hook_id'],
                    secret=secret
                )
                wh_record = self.repo.create_webhook_record(wh_record_data)