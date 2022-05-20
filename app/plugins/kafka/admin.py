from kafka import KafkaAdminClient
from kafka.admin import NewTopic

from app.config import settings

topic = NewTopic(name=settings.KAFKA_TOPIC_POST_VIEWS,
                 num_partitions=1,
                 replication_factor=1)
admin = KafkaAdminClient(
    bootstrap_servers=settings.KAFKA_ADMIN_BOOTSTRAP_URL
)

if __name__ == '__main__':
    admin.create_topics([topic])
