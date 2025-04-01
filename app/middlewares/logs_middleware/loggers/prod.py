import logging
import os
from logging.handlers import TimedRotatingFileHandler

from middlewares.logs_middleware.loggers.base import BaseLogger


class ProdLogger(BaseLogger):
	logs_dir: str = 'logs'
	log_filename: str = 'logs.log'

	def setup_handler(self):
		os.makedirs(self.logs_dir, exist_ok=True)
		log_path = os.path.join(self.logs_dir, self.log_filename)

		handler = TimedRotatingFileHandler(
			log_path,
			when='MIDNIGHT',
			interval=1,
			backupCount=3,
			encoding='utf-8',
			utc=True,
		)
		handler.namer = self._flip_name

		handler.setFormatter(
			logging.Formatter(
				fmt='[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s',
				datefmt='%Y-%m-%d %H:%M:%S',
			)
		)
		handler.setLevel(logging.INFO)
		self.logger.addHandler(handler)

	@staticmethod
	def _flip_name(log_path: str) -> str:
		log_dir, log_filename = os.path.split(log_path)
		_, timestamp = log_filename.rsplit('.', 1)
		return os.path.join(log_dir, f'logs-{timestamp}.log')
