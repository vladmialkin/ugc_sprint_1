from faststream.kafka import KafkaBroker


kafka_conn: KafkaBroker | None = None


async def get_kafka() -> KafkaBroker | None:
    return kafka_conn
