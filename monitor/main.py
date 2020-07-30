import logging
import argparse

import src.settings as settings
from src.producer import Producer
from src.consumer import Consumer

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A website health monitoring service.')

    subparsers = parser.add_subparsers(dest='client_type')

    parser_producer = subparsers.add_parser(
        'producer',
        help='A Kafka client that produces measurements of the website health.'
    )
    parser_producer.add_argument('website', help='The URL to the website to monitor.')
    parser_producer.add_argument('--pattern', help='The regex pattern to search in the page source (optional).')
    parser_producer.add_argument('--interval', type=float, help='How often to check the website (default 5 secs).')

    parser_consumer = subparsers.add_parser(
        'consumer',
        help='A Kafka client that stores the website health measurements in a database.'
    )
    # TODO: combine the usage descriptions for all parsers in the root parser

    args = parser.parse_args()

    kafka_env = settings.KAFKA_HOST, settings.KAFKA_PORT,

    if args.client_type == 'producer':
        client = Producer(
            *kafka_env,
            website=args.website,
            pattern=args.pattern,
            check_interval=args.interval
        )
    else:
        client = Consumer(*kafka_env)

    client.start()
    client.join()
