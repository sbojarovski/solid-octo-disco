from unittest import mock
from datetime import (
    datetime,
    timedelta,
)

from psycopg2 import sql
from freezegun import freeze_time

from src.models import WebsiteHealth
from src.consumer import Consumer
from src.dead_letter_handler import DeadLetterHandler
from src.resource_dispatcher import ResourceDispatcher


def test_consumer_single_message_write_to_db(model_tables, db_connection, database_model):
    with db_connection.cursor() as cur:
        cur.execute(
            sql.SQL('SELECT * FROM {};').format(
                sql.Identifier(WebsiteHealth.table_name)
            ))
        assert len(cur.fetchall()) == 0

    with mock.patch('src.consumer.KafkaConsumer') as mocked_consumer,\
            mock.patch.object(WebsiteHealth, 'database', new_callable=database_model),\
            freeze_time('2020-08-13 00:00:00 UTC'):
        mocked_message = mock.Mock()
        msg = {
            'url': 'google.com',
            'status_code': 200,
            'response_time': timedelta(seconds=0.123),
            'pattern_found': False,
            'timestamp': datetime.utcnow(),
        }
        mocked_message.value = msg
        mocked_consumer.return_value = [mocked_message]
        resource_dispatcher = ResourceDispatcher(
            dead_letter_queue=[],
        )
        consumer = Consumer(
            dispatcher=resource_dispatcher,
            name='kafka_consumer',
        )
        dlh = DeadLetterHandler(
            model_mapper=WebsiteHealth,
            dispatcher=resource_dispatcher,
            name='dead_letter_handler',
        )
        consumer.start()
        dlh.start()

        consumer.stop()
        dlh.stop()

        consumer.join()
        dlh.join()

    with db_connection.cursor() as cur:
        cur.execute(
            sql.SQL('SELECT * FROM {};').format(
                sql.Identifier(WebsiteHealth.table_name)
            ))
        existing_records = cur.fetchall()
        cols = [c.name for c in cur.description]
        record = dict(zip(cols, existing_records[0]))
        assert len(existing_records) == 1
        assert record['url'] == msg['url']
        assert record['status_code'] == msg['status_code']
        assert record['response_time'] == msg['response_time']
        assert record['pattern_found'] == msg['pattern_found']
        assert record['timestamp'] == msg['timestamp'].astimezone()


def test_consumer_dead_letter_handler():
    # TODO: write the test with a DLH
    pass
