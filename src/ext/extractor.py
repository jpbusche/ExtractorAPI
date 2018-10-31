from abc import ABC, abstractmethod
import requests
import json

class Extractor(ABC):

	url = "http://exampleofurl.com/api={}"

	@abstractmethod
	def get_game(self, identifier):
		pass

	def manipulate_data(self, data):
		pass

	def get_api(self, identifier):
		response = requests.get(self.url.format(identifier))
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			return response
		else:
			raise PageNotFound("Page not found!!!")


class PageNotFound(Exception):
	pass

class GameNotFound(Exception):
	pass