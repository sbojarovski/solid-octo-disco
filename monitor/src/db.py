import psycopg2

from pydantic import (
    BaseModel,
    PostgresDsn,
)

from src.settings import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)


class Database(BaseModel):
    dsn: PostgresDsn = \
        f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    @property
    def connection(self):
        return psycopg2.connect(self.dsn)
