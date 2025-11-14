from typing import Any, Dict, Iterator

import psycopg
from psycopg import Cursor
from psycopg.rows import dict_row

from src.pipeline.read.base import BaseReader
from src.sources.base import SourceConfig


class PostgresReader(BaseReader):
    def __init__(self, source_config: SourceConfig):
        self.connection = psycopg.connect(
            host=source_config.connection.host,
            port=source_config.connection.port,
            dbname=source_config.connection.dbname,
            user=source_config.connection.user,
            password=source_config.connection.password,
        )
        super().__init__(source_config)

    def batch_query(self, cursor: Cursor) -> Iterator[list[Dict[str, Any]]]:
        while True:
            batch = cursor.fetchmany(self.source_config.batch_size)
            if not batch:
                break
            yield list(batch)

    def read(self) -> Iterator[list[Dict[str, Any]]]:
        with self.connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(self.source_config.read.query)
            yield from self.batch_query(cursor)
