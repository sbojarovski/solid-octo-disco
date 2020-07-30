import os

KAFKA_HOST = os.environ.get('KAFKA_CONTAINER_NAME', 'kafka')
KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'website-health')
