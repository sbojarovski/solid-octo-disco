import sys
import subprocess
import time
import os

from kafka import KafkaProducer

KAFKA_HOST = os.environ.get('KAFKA_CONTAINER_NAME', 'kafka')
KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)

KAFKA_SECURITY_PROTOCOL = os.environ.get('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT')
KAFKA_SSL_CAFILE = os.environ.get('KAFKA_SSL_CAFILE', None)
KAFKA_SSL_CERTFILE = os.environ.get('KAFKA_SSL_CERTFILE', None)
KAFKA_SSL_KEYFILE = os.environ.get('KAFKA_SSL_KEYFILE', None)


success = False

while not success:
    try:
        producer = KafkaProducer(
            bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            ssl_cafile=KAFKA_SSL_CAFILE,
            ssl_certfile=KAFKA_SSL_CERTFILE,
            ssl_keyfile=KAFKA_SSL_KEYFILE,
        )
        success = True
        print(f'Kafka instance at {KAFKA_HOST}:{KAFKA_PORT} is available')
    except Exception as e:
        print(f'Could not connect to Kafka instance at {KAFKA_HOST}:{KAFKA_PORT}. Retrying in 5 secs...')
        time.sleep(5)

subprocess.run(sys.argv[1:])
