import requests
import json
import sys
from extractor import Extractor

class SteamAPI(Extractor):

	def get_game(self, identifier):
		url = 'https://store.steampowered.com/api/appdetails/?appids=' + str(identifier)
		response = requests.get(url)
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			data = response[str(identifier)]
			if data['success']:
				print(data)
			else:
				raise Exception("Jogo não encontrado!!!")
		else:
			raise Exception("Página não encontrada!!!")

a = SteamAPI()
try: 
	a.get_game(730)
except Exception as error:
	print(error)