import psycopg2

import src.settings as settings


class Database:
    @property
    def connection_kwargs(self):
        kwargs = {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
            'dbname': settings.DB_NAME,
        }
        if settings.DB_SSL_REQUIRED:
            kwargs.update({
                'sslmode': 'verify-ca',
                'sslrootcert': settings.DB_CA_PEM,
            })
        return kwargs

    @property
    def connection(self):
        return psycopg2.connect(**self.connection_kwargs)
