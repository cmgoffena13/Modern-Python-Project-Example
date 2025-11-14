from src.pipeline.read.base import BaseReader
from src.pipeline.read.postgres import PostgresReader
from src.sources.base import SourceConfig


class ReaderFactory:
    _readers = {"postgres": PostgresReader}

    @classmethod
    def register_readers(cls, readers: list[BaseReader]) -> None:
        for reader in readers:
            cls._readers[reader.source_config.name] = reader

    @classmethod
    def get_reader(cls, source_config: SourceConfig) -> BaseReader:
        if source_config.name not in cls._readers:
            raise ValueError(f"Reader for {source_config.name} not found")
        return cls._readers[source_config.name]
