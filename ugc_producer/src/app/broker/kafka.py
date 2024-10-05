from aiokafka import AIOKafkaProducer
from fastapi import Depends
from typing import Annotated


async def get_kafka() -> AIOKafkaProducer | None:
    return kafka_producer

kafka_producer: AIOKafkaProducer | None = None

Producer = Annotated[AIOKafkaProducer, Depends(get_kafka)]

