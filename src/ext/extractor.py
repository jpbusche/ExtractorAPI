from abc import ABC, abstractmethod
from db.elastic import Elastic
import datetime
import requests
import json

class Extractor(ABC):

	url = "http://exampleofurl.com/api={}"

	@abstractmethod
	def get_game(self, identifier, flag):
		pass

	def manipulate_data_est(self, data):
		pass

	def manipulate_data_tmp(self, data, identifier):
		pass

	def get_api(self, identifier):
		response = requests.get(self.url.format(identifier))
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			return response
		else:
			raise PageNotFound("Page not found!!!")

	def temporal_data(self, identifier, value, data_name):
		elastic = Elastic('elastic:9200', 'steam')
		array = []
		try:
			game = elastic.get(identifier)
			array = game[data_name]
		except:
			array = []
		current_date = datetime.datetime.now()
		data = {}
		data['value'] = value
		data['date'] = current_date.strftime("%Y-%m-%d")
		array.append(data)
		return array


class PageNotFound(Exception):
	pass

class GameNotFound(Exception):
	pass

class DataTypeNotFound(Exception):
	pass