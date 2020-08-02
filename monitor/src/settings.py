import os

KAFKA_HOST = os.environ.get('KAFKA_CONTAINER_NAME', 'kafka')
KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'website-health')

DB_USER = os.environ.get('DB_USER', 'monitor_db_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'monitor_db_password')
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'monitor_db')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME', 'test_db')

DEAD_LETTER_RETRY_SECONDS = 5
