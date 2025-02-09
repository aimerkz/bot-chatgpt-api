import logging
from abc import ABC, abstractmethod
from typing import Optional


class BaseLogger(ABC):
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger('aiogram')
        self.logger.setLevel(logging.INFO)
        self.setup_handler()

    @abstractmethod
    def setup_handler(self) -> None:
        pass
