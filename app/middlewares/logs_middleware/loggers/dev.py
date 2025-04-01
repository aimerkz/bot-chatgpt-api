import logging

from middlewares.logs_middleware.filters import ColorFilter
from middlewares.logs_middleware.loggers.base import BaseLogger


class DevLogger(BaseLogger):
	def setup_handler(self):
		handler = logging.StreamHandler()
		handler.setFormatter(
			logging.Formatter(
				fmt='%(color)s[%(asctime)s] [%(levelname)s] [%(name)s] > %(message)s',
				datefmt='%Y-%m-%d %H:%M:%S',
			)
		)
		handler.setLevel(logging.INFO)
		handler.addFilter(ColorFilter())
		self.logger.addHandler(handler)
