import os

KAFKA_HOST = os.environ.get('KAFKA_CONTAINER_NAME', 'kafka')
KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'website-health')

KAFKA_SECURITY_PROTOCOL = os.environ.get('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT')
KAFKA_SSL_CAFILE = os.environ.get('KAFKA_SSL_CAFILE', None)
KAFKA_SSL_CERTFILE = os.environ.get('KAFKA_SSL_CERTFILE', None)
KAFKA_SSL_KEYFILE = os.environ.get('KAFKA_SSL_KEYFILE', None)

DB_USER = os.environ.get('DB_USER', 'monitor_db_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'monitor_db_password')
DB_HOST = os.environ.get('DB_CONTAINER_NAME', 'db')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'monitor_db')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME', 'test_db')
DB_SSL_REQUIRED = os.environ.get('DB_SSL_REQUIRED', False)
DB_CA_PEM = os.environ.get('DB_CA_PEM', None)

DEAD_LETTER_RETRY_SECONDS = 60
