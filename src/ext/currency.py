from ext.extractor import Extractor, GameNotFound
import json

class Currency(Extractor):

	url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}'	

	def get_game(self, identifier):
		response = self.get_api(identifier)
		data = response['response']
		if data['result'] == 1:
			result = {}
			result['currency'] = data['player_count']
			return result
		else:
			raise GameNotFound("Jogo não encontrado!!!")