from fastapi import WebSocket, status, Query
from typing import Optional
from ..redis.config import Redis


redis = Redis()

async def get_token(
    websocket: WebSocket,
    token:  Optional[str] = Query(None)
):
    print("Token:", token)
    if token is None or token == "":
        await websocket.close(code = status.WS_1008_POLICY_VIOLATION)
    
    redis_client = await redis.create_connection()
    exists_token = await redis_client.exists(token) 
    
    if exists_token == 1:
        return token
    else:
        await websocket.close(code = status.WS_1008_POLICY_VIOLATION,
            reason = "Session not authenticated or expired token"
        )