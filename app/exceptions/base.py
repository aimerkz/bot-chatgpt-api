class BaseInternalException(Exception):
	def __init__(self, message: str, code: int | None = None) -> None:
		self.message = message
		self.code = code
		super().__init__(self.message)
