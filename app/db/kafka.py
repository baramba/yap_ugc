from typing import Optional

from kafka import KafkaProducer

producer: Optional[KafkaProducer] = None


async def get_kafka_producer() -> Optional[KafkaProducer]:
    return producer
