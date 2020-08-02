import logging

import pytest
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pydantic import (
    BaseModel,
    PostgresDsn,
)

import src.settings as settings
from src.models import WebsiteHealth

log = logging.getLogger(__name__)

MODELS = [
    WebsiteHealth,
]


def _create_model_tables():
    with psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_TEST_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            for model in MODELS:
                cur.execute(model._table_definition())
    log.info('Created model tables')


def _delete_model_tables():
    with psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_TEST_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            for model in MODELS:
                cur.execute(sql.SQL(
                    'DELETE FROM {};').format(
                    sql.Identifier(model.table_name)
                ))
    log.info('Cleared model tables')


@pytest.fixture(scope='function')
def model_tables():
    _create_model_tables()
    yield
    _delete_model_tables()


def _create_test_db():
    with psycopg2.connect(
        host=settings.DB_HOST,
        dbname='template1',
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    ) as conn:

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(sql.SQL(
                'DROP DATABASE IF EXISTS {};').format(
                sql.Identifier(settings.DB_TEST_NAME)
            ))
            cur.execute(sql.SQL(
                'CREATE DATABASE {};').format(
                sql.Identifier(settings.DB_TEST_NAME)
            ))
            log.info('Test database created')


def _drop_test_db():
    with psycopg2.connect(
        host=settings.DB_HOST,
        dbname='template1',
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    ) as conn:

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(sql.SQL(
                'DROP DATABASE IF EXISTS {};').format(
                sql.Identifier(settings.DB_TEST_NAME)
            ))
            log.info('Tearing down test database')


@pytest.fixture(scope='session', autouse=True)
def session_test_db():
    _create_test_db()
    yield
    # TODO: doesn't work when one of the tests fails
    _drop_test_db()


@pytest.fixture(scope='module')
def db_connection():
    with psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_TEST_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    ) as test_db_connection:
        yield test_db_connection


@pytest.fixture(scope='function', autouse=True)
def database_model():
    class TestDatabase(BaseModel):
        dsn: PostgresDsn = \
            f'postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_TEST_NAME}'

        @property
        def connection(self):
            return psycopg2.connect(self.dsn)

    return TestDatabase
