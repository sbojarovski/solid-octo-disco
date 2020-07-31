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

    @property
    def _column_definitions(self) -> str:
        return '\n'.join([
            f'{name} {field.column_type},' for name, field in self.__fields__.items()
        ])

    @property
    def _table_definition(self) -> str:
        table_definition = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            {self._column_definitions}
        );
        """
        return table_definition

    def _create_table(self):
        try:
            with self.database.connection as conn:
                with conn.cursor() as cur:
                    cur.execute(self._table_definition)
        except Exception as e:
            log.exception(e)

    @property
    def values(self) -> List:
        return list(self.__dict__.values())

    @property
    def columns(self) -> List[str]:
        return list(self.__dict__.keys())

    @property
    def _column_values_placeholder(self):
        num_cols = len(self.columns)
        return f'({", ".join(["%s"] * num_cols)})'

    @classmethod
    def bulk_create(cls, records):
        with cls.database.connection as conn:
            with conn.cursor() as cur:
                records_values = ','.join([
                    cur.mogrify(cls._column_values_placeholder, r.values) for r in records
                ])
                insert_many_query = f"""
                INSERT INTO {cls.table_name} ({cls.columns}) VALUES {records_values}
                """
                # TODO: Dead Letter Queue
                cur.execute(insert_many_query)

    def create(self):
        with self.database.connection as conn:
            with conn.cursor() as cur:
                insert_single_query = f"""
                INSERT INTO {self.table_name} ({self.columns}) VALUES %s
                """
                query = cur.mogrify(insert_single_query, self.values)
                cur.execute(query)
