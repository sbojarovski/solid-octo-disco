import logging
import requests
import re
import json

from datetime import datetime, timedelta

from kafka import KafkaProducer

import src.settings as settings
from src.stoppable_thread import StoppableThread

log = logging.getLogger(__name__)


class Producer(StoppableThread):

    def __init__(
            self,
            *args,
            website: str,
            pattern: str = None,
            check_interval: float = None,
            **kwargs
    ):
        super().__init__(args=args, kwargs=kwargs)
        self.website = website
        self.pattern = re.compile(pattern) if pattern is not None else None
        if check_interval is None:
            self.check_interval = timedelta(seconds=5.0)
        else:
            self.check_interval = timedelta(seconds=check_interval)
        self.last_check = None
        self.producer = KafkaProducer(
            bootstrap_servers=[
                f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'
            ],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )

    def send(self, message):
        def on_send_success(record_metadata):
            topic = record_metadata.topic
            partition = record_metadata.partition
            offset = record_metadata.offset
            log.info(f'Successfully sent: {topic} {partition} {offset}')

        def on_send_error(exc):
            log.exception(exc)

        log.info(f'Attempting to send: {message}')
        self.producer.send(
            settings.KAFKA_TOPIC,
            message
        )\
            .add_callback(on_send_success)\
            .add_errback(on_send_error)

    def start(self) -> None:
        self.last_check = datetime.utcnow()
        super().start()

    def run(self):
        log.info('Started Kafka Producer')
        while True:
            if datetime.utcnow() - self.last_check >= self.check_interval:
                self.last_check = datetime.utcnow()
                with requests.get(self.website) as response:
                    if self.pattern is not None:
                        pattern_found = self.pattern.match(response.text)
                    message = {
                        'status_code': response.status_code,
                        'response_time': response.elapsed.total_seconds(),
                        'pattern_found': pattern_found if pattern_found is not None else False,
                    }
                    self.send(message)

