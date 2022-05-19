from app.plugins.kafka.consumer import consumer
from app.workers.background_jobs.posts import update_view


if __name__ == '__main__':
    consumer.consume(update_view)
