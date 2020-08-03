import logging
import json

from datetime import datetime

from kafka import KafkaProducer

import src.settings as settings

log = logging.getLogger(__name__)


def on_send_success(record_metadata):
    topic = record_metadata.topic
    partition = record_metadata.partition
    offset = record_metadata.offset
    log.info(f'Successfully sent: {topic} {partition} {offset}')


def on_send_error(exc):
    log.exception(exc)


if __name__ == '__main__':
    try:
        producer = KafkaProducer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            value_serializer=lambda m: json.dumps(m, default=str).encode('utf-8'),
            security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
            ssl_cafile=settings.KAFKA_SSL_CAFILE,
            ssl_certfile=settings.KAFKA_SSL_CERTFILE,
            ssl_keyfile=settings.KAFKA_SSL_KEYFILE,
        )
        msg = {
            'url': 'google.com',
            'status_code': 200,
            'response_time': 0.123,
            'pattern_found': False,
            'timestamp': datetime.utcnow(),
        }
        producer\
            .send(settings.KAFKA_TOPIC, msg)\
            .add_callback(on_send_success)\
            .add_errback(on_send_error)
        producer.flush()
        log.info(f'Message {msg} sent')
        print(f'Message {msg} sent')
    except Exception as e:
        log.exception(e)
