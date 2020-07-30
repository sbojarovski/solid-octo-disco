import logging
import json

from kafka import KafkaConsumer

import src.settings as settings
from src.stoppable_thread import StoppableThread

log = logging.getLogger(__name__)


class Consumer(StoppableThread):
    def __init__(self, *args, **kwargs):
        super().__init__(args=args, kwargs=kwargs)
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=[
                f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'
            ],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )

    def run(self):
        log.info('Started Kafka Consumer')
        while True:
            for message in self.consumer:
                log.info(message)
