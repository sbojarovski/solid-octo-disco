from typing import ClassVar
from unittest import mock
from unittest.mock import Mock
from datetime import (
    datetime,
    timedelta,
)

import pytest
from pydantic import (
    Field
)
from freezegun import freeze_time

from src.model_mapper import ModelMapper
from src.utils import remove_whitespace


@pytest.fixture(autouse=True)
def model_class():
    class SomeModel(ModelMapper):
        table_name: ClassVar = 'some_model'

        varchar_field: str = Field(max_length=1, description='str')
        int_field: int = Field(description='int')
        interval_field: timedelta = Field(description='timedelta')
        bool_field: bool = Field(description='bool')
        timestamp_field: datetime = Field(description='timestamp')

    yield SomeModel


@pytest.fixture(autouse=True)
def model_instance(model_class):
    with freeze_time('2020-08-13 00:00:00 UTC'):
        yield model_class(
            varchar_field='v',
            int_field=1,
            interval_field=timedelta(seconds=1),
            bool_field=True,
            timestamp_field=datetime.utcnow(),
        )


@pytest.fixture(autouse=True)
def mogrified_values():
    return [
        b"('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp)",
        b"('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp)",
    ]


def test_model_mapper_column_definitions(model_class):
    expected_definition = 'varchar_field VARCHAR(1)\n' \
                          ',int_field INT\n' \
                          ',interval_field INTERVAL\n' \
                          ',bool_field BOOL\n' \
                          ',timestamp_field TIMESTAMPTZ\n'
    assert model_class._column_definitions() == expected_definition


def test_model_mapper_table_definition(model_class):
    expected_definition = """
    CREATE TABLE IF NOT EXISTS some_model (
        id SERIAL PRIMARY KEY,
        varchar_field VARCHAR(1)
        ,int_field INT
        ,interval_field INTERVAL
        ,bool_field BOOL
        ,timestamp_field TIMESTAMPTZ
    );
    """
    expected_definition = remove_whitespace(expected_definition)
    table_definition = remove_whitespace(model_class._table_definition())
    assert expected_definition == table_definition


def test_model_mapper_values(model_instance):
    expected_values = [
        'v',
        1,
        timedelta(seconds=1),
        True,
        datetime.strptime(
            '2020-08-13 00:00:00 UTC',
            '%Y-%m-%d %H:%M:%S %Z'
        ),
    ]
    assert expected_values == model_instance.values


def test_model_mapper_column_values_placeholder(model_class):
    expected_placeholder = "(%s, %s, %s, %s, %s)"
    assert expected_placeholder == model_class._column_values_placeholder()


def test_model_mapper_bulk_create(model_class, model_instance, mogrified_values):
    with mock.patch.object(model_class, 'database') as mocked_database:
        mocked_database.connection.__enter__().cursor().__enter__().mogrify = \
            Mock(
                side_effect=mogrified_values
            )
        mocked_execute = mocked_database.connection.__enter__().cursor().__enter__().execute
        expected_query = """
        INSERT INTO some_model (varchar_field, int_field, interval_field, bool_field, timestamp_field)
        VALUES
            ('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp),
            ('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp)
        ;"""
        model_class.bulk_create([model_instance, model_instance])

        insert_query = mocked_execute.call_args.args[0]
        assert mocked_execute.called
        assert remove_whitespace(expected_query) == remove_whitespace(insert_query)


def test_model_mapper_create(model_class, model_instance):
    """
    NOTE: not the best example of a test, but the actual database integration
    will be tested in the integration tests.
    """
    with mock.patch.object(model_class, 'database') as mocked_database:
        mocked_database.connection.__enter__().cursor().__enter__().mogrify = \
            Mock(
                return_value="""
                INSERT INTO some_model
                    (varchar_field, int_field, interval_field, bool_field, timestamp_field)
                VALUES
                    ('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp)
                ;                
                """
            )
        mocked_execute = mocked_database.connection.__enter__().cursor().__enter__().execute
        model_class.create(model_instance)
        expected_query = """
        INSERT INTO some_model
            (varchar_field, int_field, interval_field, bool_field, timestamp_field)
        VALUES
            ('v', 1, '0 days 1.000000 seconds'::interval, true, '2020-07-31T19:45:16.145506'::timestamp)
        ;
        """

        insert_query = mocked_execute.call_args.args[0]
        assert mocked_execute.called
        assert remove_whitespace(expected_query) == remove_whitespace(insert_query)
