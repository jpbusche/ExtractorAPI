from abc import ABC, abstractmethod

class Extractor(ABC):

	@abstractmethod
	def get_game(self, identifier):
		pass