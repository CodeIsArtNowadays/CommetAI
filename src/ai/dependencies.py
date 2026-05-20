from openai import AsyncOpenAI
from fastapi import Depends

from config import settings
from src.ai.service import AiService


async def get_openai_client():
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENAI_TOKEN
    )
    yield client
    await client.close()

async def get_ai_service(client: AsyncOpenAI = Depends(get_openai_client)):
    return AiService(client) 
    