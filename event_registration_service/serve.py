from faststream import FastStream
from faststream.kafka import KafkaBroker
import asyncio
import uuid
import json

broker = KafkaBroker("127.0.0.1:9094")

id = str(uuid.uuid4())
print(id)


async def pub():
    async with broker as br:
        # await br.publish(key=b'persons', message="genres", topic="click")
        await br.publish(key=b'60056ac8-62f3-420b-8c1a-73deaaa6e54b', message="333", topic="film_click")


asyncio.run(pub())