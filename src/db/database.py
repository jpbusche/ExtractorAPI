from abc import ABC, abstractmethod

class Database(ABC):

	@abstractmethod
	def update(self, identifier, data):
		pass

	@abstractmethod
	def get(self, identifier):
		pass

	@abstractmethod
	def delete(self, identifier):
		pass

class DataNotFound(Exception):
	pass