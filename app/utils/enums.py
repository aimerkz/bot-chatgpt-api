from enum import Enum


class ActionsEnum(str, Enum):
	EXIT = 'menu:exit'
	ASK = 'menu:ask'
	ASK_AGAIN = 'menu:ask_again'
	NEW_QUESTION = 'menu:new_question'
	GENERATE_IMAGE = 'menu:generate_image'
