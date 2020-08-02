import logging
from typing import (
    ClassVar,
    List,
)

from pydantic import BaseModel
from pydantic.fields import ModelField

from src.db import Database

log = logging.getLogger(__name__)

DEFAULT_VARCHAR_LENGTH = 255


@property
def column_type(self):

    max_length = DEFAULT_VARCHAR_LENGTH
    if hasattr(self.type_, 'max_length'):
        max_length = self.type_.max_length
    TYPE_MAP = {
        'str': f'VARCHAR({max_length})',
        'int': 'INT',
        'timedelta': 'INTERVAL',
        'bool': 'BOOL',
        'timestamp': 'TIMESTAMPTZ',
    }

    return TYPE_MAP[self.field_info.description]


setattr(ModelField, 'column_type', column_type)


class ModelMapper(BaseModel):

    table_name: ClassVar = None
    database: ClassVar = Database()

    @classmethod
    # TODO: would have been nice to have these as class properties (instead of methods)
    def _column_definitions(cls) -> str:
        return ','.join([
            f'{name} {field.column_type}\n' for name, field in cls.__fields__.items()
        ])

    @classmethod
    def _table_definition(cls) -> str:
        table_definition = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id SERIAL PRIMARY KEY,
            {cls._column_definitions()}
        );
        """
        return table_definition

    @classmethod
    def _create_table(cls):
        try:
            with cls.database.connection as conn:
                with conn.cursor() as cur:
                    cur.execute(cls._table_definition())
        except Exception as e:
            log.exception(e)

    @property
    def values(self) -> List:
        return list(self.__dict__.values())

    @classmethod
    def columns(cls) -> List[str]:
        return list(dict(cls.__dict__.items())['__fields__'].keys())

    @classmethod
    def _column_values_placeholder(cls):
        num_cols = len(cls.columns())
        return f'({", ".join(["%s"] * num_cols)})'

    @classmethod
    def bulk_create(cls, records: List):
        """
        Inserts multiple records to the database
        """
        with cls.database.connection as conn:
            with conn.cursor() as cur:
                mogrified_values = ','.join([
                    cur.mogrify(cls._column_values_placeholder(), r.values).decode('utf-8') for r in records
                ])
                insert_many_query = f"""
                INSERT INTO {cls.table_name} ({', '.join(cls.columns())}) VALUES {mogrified_values}
                ;"""
                # TODO: Dead Letter Queue
                cur.execute(insert_many_query)

    @classmethod
    def create(cls, record):
        """
        Inserts one record to the database.
        """
        with cls.database.connection as conn:
            with conn.cursor() as cur:
                insert_single_query = f"""
                INSERT INTO {cls.table_name}
                    ({cls.columns()})
                VALUES
                    {cls._column_values_placeholder()}
                ;
                """
                query = cur.mogrify(insert_single_query, record.values)
                cur.execute(query)

    def save(self):
        """
        NOTE: Deliberately not implemented.
        Saving (updating) is meant to be called on an instance of a method,
        and would also require to map out the retrieving of objects from the database.
        At that point I might as well use a fully implemented ORM.
        :return:
        """
        raise NotImplementedError
