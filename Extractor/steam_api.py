import requests
import json
import datetime
from extractor import Extractor

class SteamAPI(Extractor):

	def get_game(self, identifier):
		url = 'https://store.steampowered.com/api/appdetails/?appids=' + str(identifier)
		response = requests.get(url)
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			data = response[str(identifier)]
			if data['success']:
				result = {}
				result['name'] = data['data']['name']
				result['steam_id'] = data['data']['steam_appid']
				if data['data']['is_free'] or data['data']['price_overview'] is None:
					result['price'] = 0.0
				else:
					result['price'] = data['data']['price_overview']['initial'] / 100.0
				result['description'] = data['data']['short_description']
				result['genres'] = []
				result['publishers'] = []
				result['developers'] = []
				for genre in data['data']['genres']:
					result['genres'].append(genre['description'])
				for publisher in data['data']['publishers']:
					result['publishers'].append(publisher)
				for develop in data['data']['developers']:
					result['developers'].append(develop)
				if data['data']['release_date']['date'] != "":
					result['date'] = data['data']['release_date']['date']
				else:
					result['date'] = '12 Set, 2003'
				return json.dumps(result)
			else:
				raise Exception("Jogo não encontrado!!!")
		else:
			raise Exception("Página não encontrada!!!")