from email import message
from itertools import product
from multiprocessing.forkserver import read_signed
from urllib import response
from src.schema.chat import Message
from src.redis.config import Redis
import asyncio
from src.redis.cache import Cache
from src.model.gptj import GPT
from src.redis.producer import Producer
from src.redis.stream import StreamConsumer

redis = Redis()

async def main():
    json_client = redis.create_rejson_connection()
    redis_client = await redis.create_connection()
    consumer = StreamConsumer(redis_client)
    cache = Cache(json_client)
    producer = Producer(redis_client)

    print("Stream consumer started")
    print("Stream waiting for new messages")


    while True:
        response = await consumer.consume_stream(stream_channel="message_channel",
        count = 1,
        block= 0)

        for stream, messages in response:
            # Obtener el mensaje del stream y extraer token y los datos del mensaje
            for message in messages:
                message_id = message[0]
                token = [ k.decode('utf-8') for k, v in message[1].items()][0]
                message = [ v.decode('utf-8') for k, v in message[1].items()][0]
                
                print('Token: ', token)

                msg = Message(msg= message)

                await cache.add_message_to_cache(
                    token= token,
                    source= "human",
                    message_data = msg.dict())
            
                data = await Cache(json_client).get_chat_history(token = token)
                print("Cache: ", data)

                # Clean message
                message_data = data['messages'][-4:]

                input = ["" + i['msg'] for i in message_data]

                input = "".join(input)

                res = GPT().query(input = input)

                msg = Message(
                    msg = res
                )

                print("msg:", msg)
                
                stream_data = {}
                stream_data[str(token)] = str(msg.dict())

                await producer.add_to_stream(
                    stream_data,
                    "response_channel"
                )

                await cache.add_message_to_cache(
                    token = token,
                    source= "bot",
                    message_data= msg.dict()
                    )
                # Delete message

                await consumer.delete_message(stream_channel= "message_channel", message_id = message_id)

if __name__ == "__main__":
    asyncio.run(main())