import logging
import argparse

import src.settings as settings
from src.producer import Producer
from src.consumer import Consumer
from src.resource_dispatcher import ResourceDispatcher
from src.dead_letter_handler import DeadLetterHandler
from src.models import WebsiteHealth


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

    if args.client_type == 'producer':
        threads = [
            Producer(
                website=args.website,
                pattern=args.pattern,
                check_interval=args.interval,
                name='kafka_producer',
            ),
        ]
    else:
        resource_dispatcher = ResourceDispatcher(
            dead_letter_queue=[],
        )
        threads = [
            Consumer(
                dispatcher=resource_dispatcher,
                name='kafka_consumer',
            ),
            DeadLetterHandler(
                model_mapper=WebsiteHealth,
                dispatcher=resource_dispatcher,
                name='dead_letter_handler',
            )
        ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
