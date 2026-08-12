import hashlib
import uuid
import hmac

import httpx
from loguru import logger

from config import settings
from src.ai.service import AiService
from src.board.repository import CommitRepository
from src.core.exceptions import GithubApiException, GithubUnAutharize


class WebhookService:
    def __init__(self, ai_service: AiService, commit_repo: CommitRepository):
        self.ai_service = ai_service
        self.commit_repo = commit_repo

    async def create_webhook(self, repo_full_name: str, owner_github_token: str):
        url = f"https://api.github.com/repos/{repo_full_name}/hooks"
        headers = {
            "Authorization": f"Bearer {owner_github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        secret = str(uuid.uuid4())

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json={
                    "name": "web",
                    "active": True,
                    "events": ["push"],
                    "config": {
                        "secret": secret,
                        "url": settings.webhook_url,
                        "content_type": "json",
                    },
                },
            )

            if response.status_code != 201:
                logger.error(f"GitHub webhook creation failed [{response.status_code}]: {response.text}")
                logger.warning(response.text)
                raise GithubApiException(status_code=response.status_code)


            response_data = response.json()

            return {"wh_id": response_data["id"], "secret": secret}

    async def verify_webhook_request(
        self, signature: str | None, project_webhook_secret: str, body: bytes
    ):
        if not signature:
            raise GithubApiException(401)

        expected = (
            "sha256="
            + hmac.new(
                project_webhook_secret.encode(), body, hashlib.sha256
            ).hexdigest()
        )
        # logger.info(f'Webhook | Verify | {expected} | {signature}')
        # logger.info(f'Secret from DB: [{project_webhook_secret}]')
        # logger.info(f'Body length: {len(body)}')
        # logger.info(f'Expected: {expected}')
        # logger.info(f'Got: {signature}')


        if not hmac.compare_digest(expected, signature):
            raise GithubUnAutharize()
        return True
