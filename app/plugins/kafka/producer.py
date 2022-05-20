from confluent_kafka import Producer
from app.config import settings
import json


class KafkaProducer():
    def __init__(self, producer: Producer, topic: str):
        self.producer = producer
        self.topic = topic

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()))

    def produce(self, data):

        self.producer.produce(
            topic=self.topic,
            value=json.dumps(data),
            callback=self.delivery_report)
        self.producer.poll(0.0)

        self.producer.flush()


producer = KafkaProducer(
    Producer(**settings.KAFKA_PRODUCER_CONFIG),
    settings.KAFKA_TOPIC_POST_VIEWS
)
