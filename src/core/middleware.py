import time

from loguru import logger
from fastapi import Request


async def logging_middleware(request: Request, call_next):
    
    logger.info(f'Path {request.url} | Method {request.method}')
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    response_time = time.perf_counter() - start_time
    
    logger.info(f'Response {response.status_code} | Time {response_time}')
    return response
    
    
