from ext.extractor import Extractor, GameNotFound, DataTypeNotFound
import json

class Currency(Extractor):

	url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}'	

	def get_game(self, identifier, flag):
		response = self.get_api(identifier)
		data = response['response']
		if data['result'] == 1:
			result = {}
			if flag == 'estastic':
				return result
			elif flag == 'temporal':
				result['currency'] = self.temporal_data(identifier, data['player_count'], 'currency')
				return result
			else:
				raise DataTypeNotFound('Data type not found!!!')
		else:
			raise GameNotFound("Game not found!!!")