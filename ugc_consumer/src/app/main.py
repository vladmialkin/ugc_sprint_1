import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from aiohttp import ClientSession
from aiochclient import ChClient

from app.schemas.events import Click, UsingSearchFilters, WatchToTheEnd, ChangeVideoQuality, TimeOnPage, PageView
from app.settings.kafka import settings as kafka_settings
from app.settings.clickhouse import settings as clickhouse_settings

tables = {
    'click': Click,
    'page_view': PageView,
    'time_on_page': TimeOnPage,
    'change_video_quality': ChangeVideoQuality,
    'watch_to_the_end': WatchToTheEnd,
    'using_search_filters': UsingSearchFilters,
}

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


async def insert_into_clickhouse(table_name, schema, client):
    fields = schema.__dict__.keys()
    values = [getattr(schema, field) for field in fields]

    query = f'INSERT INTO default.{table_name} VALUES'

    await client.execute(query, tuple(values))
    logging.info('Данные добавлены')


async def consume():
    consumer = AIOKafkaConsumer(
        *kafka_settings.TOPIC_NAMES.split(','),
        bootstrap_servers=kafka_settings.KAFKA_BROKER,
        auto_offset_reset='earliest',
        group_id='my-group'
    )

    # Запустите consumer
    await consumer.start()
    async with ClientSession() as session:
        client = ChClient(session, url=clickhouse_settings.DSN)
        try:
            async for message in consumer:
                data = json.loads(message.value)
                table = data.get('event_type')
                schema = tables.get(table)(**data)
                await insert_into_clickhouse(table, schema, client)
        finally:
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
