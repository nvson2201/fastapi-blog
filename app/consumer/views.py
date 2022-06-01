from confluent_kafka import Consumer
from app.config import settings
from app.plugins.kafka.consumer import KafkaConsumer
from app.services.posts import post_services


def update_view(msg):
    post_services.update_views(msg['id'])


if __name__ == '__main__':
    views_consumer = KafkaConsumer(Consumer(
        settings.KAFKA_CONSUMER_CONFIG),
        settings.KAFKA_TOPIC_POST_VIEWS
    )
    views_consumer.consume(update_view)
