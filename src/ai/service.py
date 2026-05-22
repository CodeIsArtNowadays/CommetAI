from openai import AsyncOpenAI

from src.ai.prompts import summarize_commit_system_prompt, describe_project_system_prompt
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
        return response.content

    async def summarize_commit(self, commit_info: str):
        
        user_prompt = f'Commit to analyse: {commit_info}'
        
        messages = [
            {'role': 'system', 'content': summarize_commit_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        answer = await self.ask_llm(messages)
        if not answer:
            raise LLMException
        return answer

    async def describe_project(self, diff: str):
        user_prompt = f'Describe project by this first commit {diff}'
        messages = [
            {'role': 'system', 'content': describe_project_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        if messages:
            pass
    
    
            
# commits = list[]
# llm -> for commit -> summary commit
# create next logical task based on last commit