
DC_BASE = docker-compose.yml
DC_DB = docker-compose.db.yml
DC_DEV = docker-compose.dev.yml
DC_TEST = docker-compose.test.yml

DC_DB_FILES = -f $(DC_BASE) -f $(DC_DB)
DC_DEV_FILES = $(DC_DB_FILES) -f $(DC_DEV)
DC_TEST_FILES = $(DC_DB_FILES) -f $(DC_TEST)

build-dev:
	docker-compose $(DC_DEV_FILES) build

build-test:
	docker-compose $(DC_TEST_FILES) build

run-dev: build-dev
	docker-compose $(DC_DEV_FILES) up

run-test: build-test
	docker-compose $(DC_DB_FILES) start db && \
	docker-compose $(DC_TEST_FILES) run test && \
	docker-compose $(DC_DB_FILES) stop db
