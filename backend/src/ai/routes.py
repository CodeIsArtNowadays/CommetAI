from fastapi import APIRouter, Depends

from src.ai.dependencies import get_ai_service
from src.ai.service import AiService


ai_router = APIRouter()


@ai_router.get('/ai')
async def ai(ai_service: AiService = Depends(get_ai_service)):
    messages = [
        {
            'role': 'user',
            'content': 'tell me about unicorns in 5 sentences'
        }
    ]
    
    return await ai_service.ask_llm(messages)