from confluent_kafka import Consumer
from app.config import settings
from app.plugins.kafka.consumer import KafkaConsumer


def create_notifications(msg):
    pass
    # find all follower

    # content = msg['content']
    # sender_id = msg['sender_id']
    # post_id = msg['post_id']

    # send message for all followers


if __name__ == '__main__':
    views_consumer = KafkaConsumer(Consumer(
        settings.KAFKA_CONSUMER_CONFIG),
        settings.KAFKA_TOPIC_POST_NOFICATIONS
    )
    views_consumer.consume(create_notifications)
