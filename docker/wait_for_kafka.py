import sys
import subprocess
import time
import os

from kafka import KafkaProducer

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'kafka')
KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)

success = False

while not success:
    try:
        producer = KafkaProducer(bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'])
        success = True
        print(f'Kafka instance at {KAFKA_HOST}:{KAFKA_PORT} is available')
    except Exception as e:
        print('Could not connect to Kafka instance at {KAFKA_HOST}:{KAFKA_PORT}. Retrying in 5 secs...')
        time.sleep(5)

subprocess.run(sys.argv[1:])
