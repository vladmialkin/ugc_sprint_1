from fastapi import APIRouter

from app.db import clickhouse
from app.repositories.clickhouse_repository import ClickHouseRepository

router = APIRouter()


@router.get("/get_data")
async def get_data():
    repository = ClickHouseRepository(clickhouse.client)
    data = await repository.get_data()
    for val in data.items():
        print(val)
    return {'ОК'}
