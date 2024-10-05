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


async def create_tables(client):
    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.click (
        event_type String,
        user_id String,
        element_id String,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')

    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.page_view (
        event_type String,
        user_id String,
        page_id String,
        element_id String,
        element_info String,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')

    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.time_on_page (
        event_type String,
        user_id String,
        element_id String,
        element_info String,
        duration Int32,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')

    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.change_video_quality (
        event_type String,
        user_id String,
        video_id String,
        quality_before Int32,
        quality_after Int32,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')

    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.watch_to_the_end (
        event_type String,
        user_id String,
        video_id String,
        duration Int32,
        viewed Int32,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')

    await client.execute('''
    CREATE TABLE IF NOT EXISTS default.using_search_filters (
        event_type String,
        user_id String,               
        filters String,            
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at)
    ''')


async def insert_into_clickhouse(table_name, schema, client):
    fields = schema.__dict__.keys()
    values = [getattr(schema, field) for field in fields]

    query = f'INSERT INTO default.{table_name} VALUES'

    await client.execute(query, tuple(values))
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
        await create_tables(client)
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
