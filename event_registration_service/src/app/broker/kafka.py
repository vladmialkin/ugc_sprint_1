# from faststream.kafka import KafkaBroker
#
#
# kafka_conn: KafkaBroker | None = None
#
#
# async def get_kafka() -> KafkaBroker | None:
#     return kafka_conn


from aiokafka import AIOKafkaProducer


kafka_producer: AIOKafkaProducer | None = None


async def get_kafka() -> AIOKafkaProducer | None:
    return kafka_producer
