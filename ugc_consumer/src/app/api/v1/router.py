from app.api.v1.routers.kafka import router as kafka_router
from fastapi import APIRouter

router = APIRouter(prefix="/api/ugc/v1")

router.include_router(kafka_router, prefix="/ugc", tags=["Получение данных из Kafka"])
