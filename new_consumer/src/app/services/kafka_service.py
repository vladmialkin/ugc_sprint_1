import json

from app.repositories.clickhouse_repository import ClickHouseRepository


class KafkaService:
    def __init__(self, clickhouse_repository: ClickHouseRepository, consumer):
        self.clickhouse_repository = clickhouse_repository
        self.consumer = consumer

    async def consume(self):
        async for message in self.consumer:
            data = message.value.decode("utf-8")
            data = data.replace("'", '"')
            json_data = json.loads(data)
            await self.clickhouse_repository.save_data(json_data)
