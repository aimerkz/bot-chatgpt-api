import logging


class ColorFilter(logging.Filter):
	COLOR = {
		'DEBUG': '\033[92m',  # Зеленый
		'INFO': '\033[92m',  # Зеленый
		'WARNING': '\033[93m',  # Желтый
		'ERROR': '\033[91m',  # Красный
		'CRITICAL': '\033[91m',  # Красный
	}

	def filter(self, record) -> bool:
		record.color = self.COLOR[record.levelname]
		return True
