import requests
import json
from elasticsearch import Elasticsearch
from db.database import Database, DataNotFound

class Elastic(Database):

	def __init__(self, host, index):
		self.hostname = host
		self.index_name = index
		try:
			self.elastic = self.connect_elasticsearch()
		except ElasticNotConnected as enc:
			raise ElasticNotConnected('Elasticsearch couldn\'t be connected!!!')

	def get(self, identifier):
		res = self.elastic.search(index=self.index_name, body={"query": {"match": {"steam_id": int(identifier)}}})
		if res['hits']['total'] == 1:
			data = res['hits']['hits'][0]['_source']
			return data
		else:
			raise DataNotFound('Data has not found in the Database!!!')

	def update(self, identifier, data):
		if self.has_data(identifier):
			body = {}
			body['doc'] = data
			self.elastic.update(index=self.index_name, doc_type='game', id=identifier, body=body)
		else:
			self.elastic.index(index=self.index_name, doc_type='game', id=identifier, body=data)

	def delete(self, identifier):
		url = 'http://{}/{}/game/{}'
		response = requests.delete(url.format(self.hostname, self.index_name, identifier))
		if response.status_code != requests.codes.ok:
			raise DataNotFound('Data has not found in the Database!!!')

	def has_data(self, identifier):
		url = 'http://{}/{}/game/{}'
		response = requests.get(url.format(self.hostname, self.index_name, identifier))
		if response.status_code == requests.codes.ok:
			return True
		else:
			return False
	
	def connect_elasticsearch(self):
		elastic = Elasticsearch([self.hostname])
		if elastic.ping():
			return elastic
		else:
			raise ElasticNotConnected('Elasticsearch couldn\'t be connected!!!')

	def delete_index(self):
		self.elastic.indices.delete(index=self.index_name, ignore=[400, 404])

	def get_all(self):
		res = self.elastic.search(index=self.index_name, body={"query": {"match_all":{}}})
		size = res['hits']['total']
		res = self.elastic.search(index=self.index_name, body={"size": size, "query": {"match_all":{}}})
		games = []
		for game in res['hits']['hits']:
			pair = (int(game['_id']), game['_source']['name'])
			games.append(pair)
		return games


class ElasticNotConnected(Exception):
	pass