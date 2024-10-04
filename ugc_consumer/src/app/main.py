import asyncio

from aiochclient import ChClient
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from app.api.v1.deps.session import Session
from app.api.v1.routers.kafka import router
from contextlib import asynccontextmanager

from app.repositories.clickhouse_repository import ClickHouseRepository
from app.services.kafka_service import KafkaService
from app.settings.kafka import settings as kafka_settings
from app.db import kafka, clickhouse


@asynccontextmanager
async def lifespan(_: FastAPI):
    session = Session()

    clickhouse.client = ChClient(session)

    clickhouse_repository = ClickHouseRepository(clickhouse.client)

    kafka.consumer = AIOKafkaConsumer(
        kafka_settings.TOPIC_NAME,
        bootstrap_servers=kafka_settings.KAFKA_BROKER
    )
    await kafka.consumer.start()
    kafka_service = KafkaService(consumer=kafka.consumer, clickhouse_repository=clickhouse_repository)
    loop = asyncio.get_event_loop()
    loop.create_task(kafka_service.consume())
    yield
    await kafka.consumer.stop()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/ugc/docs",
    openapi_url="/api/ugc/openapi.json",
)

app.include_router(router)
