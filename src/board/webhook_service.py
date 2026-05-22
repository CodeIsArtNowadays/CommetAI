import hashlib
import uuid
import json
import hmac

import httpx

from config import settings
from src.ai.service import AiService
from src.board.repository import CommitRepository
from src.core.exceptions import GithubApiException, GithubUnAutharize
from src.board.schemas import CommitCreateSchema


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

            if not response.status_code == 201:
                raise GithubApiException(status_code=response.status_code)

            response_data = response.json()

            return {"wh_id": response_data["id"], "secret": secret}

    async def get_diffs_from_commits(
        self, commits: list, repo_full_name: str, owner_github_token: str
    ):
        diffs = []
        async with httpx.AsyncClient() as client:
            for commit in commits:
                commit_id = commit["id"]
                url = (
                    f"https://api.github.com/repos/{repo_full_name}/commits/{commit_id}"
                )
                headers = {
                    "Authorization": f"Bearer {owner_github_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
                response = await client.get(url, headers=headers)

                response_data = response.json()

                diff_data = {
                    "sha": response_data["sha"],
                    "commit_message": response_data.get("commit").get("message"),
                    "commit_author_name": response_data.get("commit")
                    .get("author")
                    .get("name"),
                    "commit_created": response_data.get("commit")
                    .get("author")
                    .get("date"),
                    "additions": response_data.get("stats").get("additions"),
                    "deletions": response_data.get("stats").get("deletions"),
                    "files": response_data.get("files"),
                }

                diffs.append(diff_data)
        return diffs

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

        if not hmac.compare_digest(expected, signature):
            raise GithubUnAutharize()
        print("Verified")
        return True
    
    async def handle_push(self, data: dict):
        commits_raw = data["commits"]
        repo_full_name = data["repo_full_name"]
        owner_github_token = data["owner_github_token"]

        commits = await self.get_diffs_from_commits(
            commits_raw, repo_full_name, owner_github_token
        )

        for commit in commits:
            answer = await self.ai_service.summarize_commit(commit)

            answer = json.loads(answer)

            commit_data = CommitCreateSchema(
                commit_info=str(commit),
                project_id=data["project_id"],
                sha=commit["sha"],
                summary=answer["summary"],
                technical=answer["technical"],
                process=answer["process"],
                risks=answer["risks"],
                conventional_commits=answer["conventional_commits"],
                author=answer["author"],
            )

            await self.commit_repo.create(commit_data)
            
            existing_tasks = []
            task = await self.ai_service.create_task(commit_data.summary, existing_tasks)
            
            print(task)
        # if not data["project_description"]:
        #     description = await self.ai_service.describe_project('asd')
        
        return {"status": "ok"}
