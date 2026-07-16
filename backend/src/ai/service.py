import json
import time

from loguru import logger
from openai import AsyncOpenAI

from src.ai.prompts import create_task_system_prompt, summarize_commit_system_prompt, describe_project_system_prompt
from src.core.exceptions import LLMException


class AiService:
    def __init__(self, client: AsyncOpenAI):
        
        self.client = client
        self.model = 'openai/gpt-4.1-nano'
        
    async def ask_llm(self, messages):
        logger.info(f'AI | model {self.model}')
        start_time = time.perf_counter()
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        logger.info(f'AI | Respond time: {time.perf_counter() - start_time}')
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

    async def create_task(self, commit_summary: str, tasks: list):
        user_prompt = f'Last commit summary: {commit_summary}. Already existing tasks: {tasks}'
        
        messages = [
            {'role': 'system', 'content': create_task_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        
        answer = await self.ask_llm(messages)
        answer = json.loads(answer)
        return answer
    
    async def create_project_description(self, commits: list, project_title: str):
        user_prompt = f'Project: {project_title}, first 5 commits: {commits}'
        
        messages = [
            {'role': 'system', 'content': describe_project_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        
        return json.loads(await self.ask_llm(messages))
