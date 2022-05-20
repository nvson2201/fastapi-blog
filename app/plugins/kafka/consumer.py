from confluent_kafka import Consumer, KafkaException
import json
from app.config import settings


class KafkaConsumer():
    def __init__(self, comsumer: Consumer, topic: str):
        self.consumer = comsumer
        self.topic = topic
        self.consumer.subscribe([topic])

    def consume(self, back_ground_job):

        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                msg = json.loads(msg.value())
                back_ground_job(msg)

        self.consumer.close()


consumer = KafkaConsumer(Consumer(
    settings.KAFKA_CONSUMER_CONFIG),
    settings.KAFKA_TOPIC_POST_VIEWS
)
