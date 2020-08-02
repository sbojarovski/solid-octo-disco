import logging
import json

from kafka import KafkaConsumer

import src.settings as settings
from src.stoppable_thread import StoppableThread
from src.models import WebsiteHealth
from src.resource_dispatcher import ResourceDispatcher

log = logging.getLogger(__name__)


class Consumer(StoppableThread):
    def __init__(self,
                 *args,
                 dispatcher: ResourceDispatcher,
                 **kwargs
                 ):
        super().__init__(args=args, kwargs=kwargs)
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=[
                f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'
            ],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )
        self.dispatcher = dispatcher

    def run(self):
        log.info('Started Kafka Consumer')
        while True:
            for message in self.consumer:
                log.info(f'Received {message} from Kafka')
                try:
                    wh = WebsiteHealth(
                        **message.value
                    )
                except Exception as e:
                    log.exception(e)
                    log.error(f'Could not create event instance from message:{message}')
                    continue

                try:
                    WebsiteHealth.create(wh)
                    log.info(f'Successfully saved message to database')
                except Exception as e:
                    log.exception(e)
                    log.error(f'Could not save message to database. Appending to DLQ')
                    with self.dispatcher.lock:
                        self.dispatcher.dead_letter_queue.append(wh)
