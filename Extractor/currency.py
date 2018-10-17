import requests
import json
from extractor import Extractor

class Currency(Extractor):

	def get_game(self, identifier):
		url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=' + str(identifier)
		response = requests.get(url)
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			data = response['response']
			if data['result'] == 1:
				result = {}
				result['currency'] = data['player_count']
				return json.dumps(result)
			else:
				raise Exception("Jogo não encontrado!!!")
		else:
			raise Exception("Página não encontrada!!!")