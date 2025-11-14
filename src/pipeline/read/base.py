from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator

from src.sources.base import SourceConfig


class BaseReader(ABC):
    def __init__(self, source_config: SourceConfig):
        self.source_config = source_config

    @abstractmethod
    def read(self) -> Iterator[list[Dict[str, Any]]]:
        pass
