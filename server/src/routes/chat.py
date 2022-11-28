
from http.client import HTTPException

import json
import os
import uuid
from fastapi import APIRouter, FastAPI, WebSocket, Request, WebSocketDisconnect, Depends


from ..schema.chat import Chat

from  rejson import Path

from ..redis.config import Redis
from ..redis.stream import StreamConsumer
from ..redis.producer import Producer
from ..redis.cache import Cache

from ..socket.connection import ConnectionManager
from ..socket.utils import get_token

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

# @route Post /token
# @desc Route to generate chat token
# @access Public

@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())
    
    if name == "":
        raise HTTPException(status_code = 400, detail = {
            "loc": "name",
            "msg": "Ingrese un nombre valido"
        })
    print("\n\n name: ",name)
    # Create new chat session
    json_client =  redis.create_rejson_connection()

    chat_session = Chat(
        token = token,
        messages= [],
        name = name
    )
    
    # Store chat session in redis JSON with the token as key
    json_client.jsonset(str(token), Path.rootPath(), chat_session.dict())

    # Set a timeout for redis data
    
    redis_client = await redis.create_connection()

    await redis_client.expire(str(token), 3600)

    return chat_session.dict()


@chat.post("/refresh_token")
async def refresh_token(request: Request, token: str):
    json_client = redis.create_rejson_connection()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)

    if data == None:
        raise HTTPException(
            status_code=400, detail="Session expired or does not exist")
    else:
        return data

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token : str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)
    json_client = redis.create_rejson_connection()
    consumer = StreamConsumer(redis_client)

    try:    
        while True:
            data = await websocket.receive_text()
            ## Send Typing event
            print("data:",data)
            await manager.send_typing_action(websocket)
            print("Se envio typing")
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data, "message_channel")
            response = await consumer.consume_stream(stream_channel= "response_channel", block = 0)
            print("response:", response)
            
            for stream, messages in response:
                for message in messages:
                    response_token = [k.decode('utf-8')
                                      for k, v in message[1].items()][0]
                    
                    if token == response_token:
                        response_message = [v.decode('utf-8').replace("'", '"')
                                            for k, v in message[1].items()][0]

                        response_json = json.loads(response_message)
                        response_json['event'] = "message"
                        print("token:", token)
                        print(response_json)
                        await manager.send_personal_message(response_json, websocket)
                    await consumer.delete_message(stream_channel="response_channel", message_id=message[0].decode('utf-8'))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    return None