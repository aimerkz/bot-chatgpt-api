import logging
from abc import ABC, abstractmethod


class BaseLogger(ABC):
	def __init__(self, logger: logging.Logger | None = None) -> None:
		self.logger = logger or logging.getLogger('aiogram')
		self.logger.setLevel(logging.INFO)
		self.setup_handler()

	@abstractmethod
	def setup_handler(self) -> None:
		pass
