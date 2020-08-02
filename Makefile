
DC_BASE = docker-compose.yml
DC_DB = docker-compose.db.yml
DC_DEV = docker-compose.dev.yml
DC_TEST = docker-compose.test.yml

DC_DB_FILES = -f $(DC_BASE) -f $(DC_DB)
DC_DEV_FILES = $(DC_DB_FILES) -f $(DC_DEV)
DC_TEST_FILES = $(DC_DB_FILES) -f $(DC_TEST)

produce_single_message = "PYTHONPATH=. python ./src/commands/produce_single_message.py"
initialize_database_tables = "PYTHONPATH=. python ./src/commands/initialize_database_tables.py"
kafka_delete_topic = "kafka-topics.sh --zookeeper zookeeper:2181 --delete --topic website-health"

build-dev:
	docker-compose $(DC_DEV_FILES) build

build-test:
	docker-compose $(DC_TEST_FILES) build

run-producer-dev: build-dev
	docker-compose $(DC_DEV_FILES) run producer

init-db-dev: build-dev
	docker-compose $(DC_DEV_FILES) run consumer bash -c $(initialize_database_tables)

run-consumer-dev: build-dev init-db-dev
	docker-compose $(DC_DEV_FILES) run consumer

run-kafka-shell-dev: build-dev
	docker-compose $(DC_DEV_FILES) run kafka bash

purge-topic-dev: build-dev
	docker-compose $(DC_DEV_FILES) run kafka bash -c $(kafka_delete_topic)

produce-single-dev: build-dev
	docker-compose $(DC_DEV_FILES) run producer bash -c $(produce_single_message)

run-dev: build-dev init-db-dev
	docker-compose $(DC_DEV_FILES) up

run-test: build-test
	docker-compose $(DC_DB_FILES) start db && \
	docker-compose $(DC_TEST_FILES) run test && \
	docker-compose $(DC_DB_FILES) stop db

run-test-shell: build-test
	docker-compose $(DC_DB_FILES) start db && \
	docker-compose $(DC_TEST_FILES) run test bash
