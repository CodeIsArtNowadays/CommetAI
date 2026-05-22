import json

from typing import Sequence
from openai import AsyncOpenAI

from src.ai.prompts import create_task_system_prompt, summarize_commit_system_prompt
from src.board.models import Task
from src.core.exceptions import LLMException


class AiService:
    def __init__(self, client: AsyncOpenAI):
        
        self.client = client
        self.model = 'openai/gpt-oss-20b:free'
        
    async def ask_llm(self, messages):
        response = await self.client.chat.completions.create(
          model="openai/gpt-oss-120b:free",
          messages=messages,
          extra_body={"reasoning": {"enabled": True}}
        )

        response = response.choices[0].message
        if not response.content:
            raise LLMException
        return response.content

    async def summarize_commit(self, commit_info: str):
        
        user_prompt = f'Commit to analyse: {commit_info}'
        
        messages = [
            {'role': 'system', 'content': summarize_commit_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        answer = await self.ask_llm(messages)
        return answer

    async def create_task(self, commit_summary: str, tasks: Sequence[Task]):
        user_prompt = f'Last commit summary: {commit_summary}. Already existing tasks: {tasks}'
        
        messages = [
            {'role': 'system', 'content': create_task_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        print(user_prompt)
        
        answer = await self.ask_llm(messages)
        answer = json.loads(answer)
        return answer
    