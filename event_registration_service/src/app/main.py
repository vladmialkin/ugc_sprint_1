from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from faststream.kafka import KafkaBroker

from app.api.v1.router import router
from app.broker import kafka
from app.settings.api import settings as api_settings
from app.settings.kafka import settings as kafka_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    kafka.kafka_conn = KafkaBroker(f"{kafka_settings.KAFKA_HOST}:{kafka_settings.KAFKA_PORT}")
    yield
    await kafka.kafka_conn.close()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(router)
