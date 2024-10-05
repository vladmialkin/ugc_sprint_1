import asyncio
import json
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


async def insert_into_clickhouse(table, schema, client):
    column_names = [field.name for field in fields(schema)]
    column_names_str = ', '.join(column_names)
    col_count = ', '.join(['%s'] * len(column_names))
    bind_values = ','.join(
        cursor.mogrify(f"({col_count})", astuple(row)) for row in data)

    query = (f'INSERT INTO {table} ({column_names_str}) VALUES {bind_values} '
             f'ON CONFLICT (id) DO NOTHING')

    await client.execute('INSERT INTO test.new_table (id, name,  year) VALUES',
                         (data["id"], data["name"], data["year"]),
                         )
    print('Данные добавлены')


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
                # table = data.get('event_type')
                table = None
                await insert_into_clickhouse(table, data, client)
        finally:
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
